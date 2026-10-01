"""Real PDF fixtures catch metadata mismatch and corrupt-source acceptance."""
import sys
from pathlib import Path
import pytest
from pypdf import PdfWriter
from pypdf.errors import PyPdfError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'reader'))
from check_inputs import checked_pdf_pages

def test_actual_pdf_pages_reject_incorrect_metadata(tmp_path):
 path=tmp_path/'formal.pdf';writer=PdfWriter()
 writer.add_blank_page(width=600,height=800);writer.add_blank_page(width=600,height=800)
 writer.write(path)
 with pytest.raises(ValueError,match='actual PDF page count 2 differs from metadata 3'):checked_pdf_pages(path,3)
 assert checked_pdf_pages(path,2)==2

def test_corrupt_pdf_cannot_satisfy_claimed_page_count(tmp_path):
 path=tmp_path/'corrupt.pdf';path.write_bytes(b'%PDF-1.7\nThis is not a valid formal PDF.')
 with pytest.raises(PyPdfError):checked_pdf_pages(path,1)
