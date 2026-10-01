#!/usr/bin/env python3
"""Serve the existing public reader snapshot using only the Python standard library."""

import argparse
import errno
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys


class SnapshotHandler(SimpleHTTPRequestHandler):
    """Keep requests within the public snapshot, including symlink targets."""

    def send_head(self):
        try:
            target = Path(self.translate_path(self.path)).resolve()
            target.relative_to(Path(self.directory).resolve())
            # SimpleHTTPRequestHandler resolves index files after directory lookup.
            if target.is_dir():
                for name in ("index.html", "index.htm"):
                    index = target / name
                    if index.exists():
                        index.resolve().relative_to(Path(self.directory).resolve())
                        break
        except (ValueError, OSError, RuntimeError):
            self.send_error(404, "File not found")
            return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404, "File not found")
        return None


def port_number(value):
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("端口必须是 0 至 65535 的整数")
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("端口必须是 0 至 65535 的整数")
    return port


def main():
    parser = argparse.ArgumentParser(description="在本机打开 reader/preview 静态阅读快照。")
    parser.add_argument("--no-browser", action="store_true", help="不自动打开浏览器")
    parser.add_argument("--port", type=port_number, default=None,
                        help="指定本机端口；0 自动分配。默认 8000，已占用时自动分配")
    args = parser.parse_args()
    project = Path(__file__).resolve().parent.parent
    snapshot = (project / "reader" / "preview").resolve()
    try:
        snapshot.relative_to(project)
    except ValueError:
        print("错误：reader/preview 指向项目之外，无法启动。", file=sys.stderr)
        return 1
    if not snapshot.is_dir() or not (snapshot / "index.html").is_file():
        print("错误：缺少 reader/preview/index.html 静态快照。请取得完整项目快照后重试。",
              file=sys.stderr)
        return 1
    handler = partial(SnapshotHandler, directory=str(snapshot))
    requested_port = 8000 if args.port is None else args.port
    try:
        try:
            server = ThreadingHTTPServer(("127.0.0.1", requested_port), handler)
        except OSError as exc:
            if args.port is None and (exc.errno == errno.EADDRINUSE or
                                      getattr(exc, "winerror", None) == 10048):
                print("默认端口 8000 已被占用，正在选择空闲本机端口。", flush=True)
                server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
            else:
                raise
    except OSError as exc:
        print("错误：无法监听本机端口 {}：{}。可使用 --port 0 自动选择端口。".format(
            requested_port, exc), file=sys.stderr)
        return 1
    with server:
        url = "http://127.0.0.1:{}/".format(server.server_address[1])
        print("阅读器地址：{}".format(url), flush=True)
        print("展示当前静态快照。按 Ctrl+C 停止服务；关闭浏览器后服务仍会运行。", flush=True)
        if not args.no_browser:
            import webbrowser
            try:
                opened = webbrowser.open(url, new=2)
            except Exception as exc:
                print("自动打开浏览器失败：{}。请手动打开上面的地址。".format(exc), flush=True)
            else:
                if not opened:
                    print("未能自动打开浏览器，请手动打开上面的地址。", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n阅读器服务已停止。", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
