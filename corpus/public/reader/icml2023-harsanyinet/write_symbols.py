from pathlib import Path
import json
B=Path(__file__).resolve().parent;P='icml2023-harsanyinet';S=[]
rows=[
('hnet-raw-game',r'g(T)',r'v(x_T)','原始掩码输出','Raw masked output',r'g(T)=v(x_T)', 'Game α',r'v(x_T)',[3,12,19],'same_definition','Harsanyi.Game'),
('hnet-output-baseline',r'b',r'v(x_\varnothing)','输出基线','Output baseline',r'b=g(\varnothing)','ℝ',r'v(x_\varnothing)',[3,12,19],'renaming','Harsanyi.centered'),
('hnet-centered-game',r'g_0(T)',r'V(T)','中心化收益','Centered reward',r'g_0(T)=g(T)-b','Game α',r'V(T)=v(x_T)-v(x_\varnothing)',[3,12],'centered_variant','Harsanyi.centered'),
('hnet-centered-dividend',r'I_{g_0}(S)',r'I(S)','中心化交互','Centered dividend',r'I_{g_0}(S)=\sum_{T\subseteq S}(-1)^{|S|-|T|}g_0(T)','ℝ',r'I(\varnothing)=0',[3,14,15],'same_definition','Harsanyi.interaction'),
('hnet-input-baseline',r'r_i',r'b_i','输入基线向量','Input baseline vector',r'(x_T)_i=\begin{cases}x_i&i\in T\\r_i&i\notin T\end{cases}','α → ℝ',r'b_i',[3,19],'renaming','Harsanyi.maskCoordinates'),
('hnet-unit-game',r'u_j(T)',r'z_u^{(l)}(x_T)','单元掩码游戏','Masked unit game',r'u_j(T)=z_j(x_T)','Game α',r'z_u^{(l)}(x_T)',[3,12,14],'renaming','Harsanyi.Network.unitGame'),
('hnet-unit-dividend',r'J_j(S)',r'J_u^{(l)}(S)','单元中心化交互','Centered unit dividend',r'J_j(S)=I_{u_j-u_j(\varnothing)}(S)','ℝ',r'J_u^{(l)}(S)',[3,12,14,15],'same_definition','Harsanyi.Network.requirement_unit_interaction'),
('hnet-receptive-field',r'R_j',r'R_u^{(l)}','感受野','Receptive field',r'R_j=\bigcup_{k\in C_j}R_k','Finset α',r'R_u^{(l)}',[3,5,13,16],'same_definition','Harsanyi.Network.receptive'),
('hnet-child-set',r'C_j',r'S_u^{(l)}','所选孩子节点','Selected child nodes',r'C_j=\{k:(\Sigma_j)_{kk}=1\}','finite node index set',r'S_u^{(l)}',[4,5,13,16],'renaming','Harsanyi.Network.Expr'),
('hnet-shapley',r'\varphi_g(i)',r'\varphi(i)','经典阶乘权重Shapley','Classical factorial-weighted Shapley',r'\varphi_g(i)=\sum_{T\subseteq N\setminus\{i\}}\frac{|T|!(|N|-|T|-1)!}{|N|!}[g(T\cup\{i\})-g(T)]','ℝ, i ∈ N',r'\varphi(i)',[3,12,13,19],'same_definition','Harsanyi.factorialShapley'),
('hnet-selected-universe',r'Q',r'\widehat N','条件归因的玩家集','Players of the conditional attribution game',r'g_Q(T)=g(T\cup(N\setminus Q))','Finset α, Q ⊆ N',r'\widehat N',[19],'renaming','Harsanyi.Network.conditional_forward_shapley'),
('hnet-reduced-field',r'R_j\cap Q',r'S\cap\widehat N','选中玩家的场','Field restricted to selected players',r'|R_j\cap Q|','Finset α',r'|S|',[19],'derived_quantity','Harsanyi.Network.conditional_receptive'),
('hnet-unit-count',r'M',r'M','单元数量与交互支撑上界','Unit count and dividend-support upper bound',r'M=\sum_lm^{(l)}','ℕ',r'M',[4,6],'same_definition','Harsanyi.Network.support_card_le_units'),
('hnet-channel-gate',r'\mathbf1_{\sum_c|z_c|\ne0}',r'\mathbf1_{\sum_c|z_c|\ne0}','分组通道非零gate','Grouped channel nonzero gate',r'\sum_c|z_c|\ne0\iff\exists c,z_c\ne0','finite real vector',r'\mathbf1_{\sum_c|z_c|\ne0}',[7,16],'conflict','Harsanyi.Network.groupedBlock')]
for id,can,orig,zh,en,definition,domain,od,pages,relation,lean in rows:
 desc=zh+'；按本篇来源作用域读取。';ed=en+'; interpreted in the source-specific scope.'
 S.append(dict(id=id,canonical_tex=can,name_zh=zh,name_en=en,definition_tex=definition,description_md=desc,type_or_domain=domain,scope='fixed input and baseline; finite masks of this paper',assumptions=['输入与参数固定，所有集合为有限。'],empty_set_convention='原I(empty)=0；原始g(empty)不默认零；空场R1/R2可为常数，实际无偏置架构恒零。',baseline_convention='原输入b_i映射r_i；原V=g0；原I=I_g0；输出b=g(empty)。',aliases=[orig],paper_mappings=[dict(paper_id=P,version_id='ver-'+P+'-formal',original_tex=orig,original_definition_tex=od,pdf_pages=pages,source_id='src-'+P+'-formal',relation_type=relation,note='groupgate与scalarAND数值不同；其余按显式定义对齐。' if relation=='conflict' else '保留源定义域和中心化约定。')],lean_names=[lean],version=1,translations={'en':dict(name_zh=en,description_md=ed,assumptions=['Inputs and parameters fixed; every coalition is finite.'],empty_set_convention='The source empty dividend is zero; the raw empty output is not assumed zero. R1/R2 allow constant empty-field units; the actual bias-free architecture makes them zero.',baseline_convention='The source input b_i maps to r_i; V is g0, I is its dividend, and scalar output b is g(empty).',paper_mappings=[dict(paper_id=P,note='Grouped and scalar AND gates differ numerically.' if relation=='conflict' else 'Preserve the source domain and centering convention.')])}))
(B/'symbols.json').write_text(json.dumps(dict(paper_id=P,symbols=S),ensure_ascii=False,indent=2)+'\n')
f=B/'content.json';d=json.loads(f.read_text());d['symbols']=S
for r in d['results']:
 r['symbol_ids']=[s['id'] for s in S]
 r['notation_map']=[dict(original=r'V(T)',canonical=r'g_0(T)',note='原reward明确中心化；不设raw baseline零。'),dict(original=r'I(S)',canonical=r'I_{g_0}(S)',note='原空交互为零；全部子集和包括空集。'),dict(original=r'b_i',canonical=r'r_i',note='输入基线向量与输出基线标量不同。')]
 r['translations']['en']['notation_map']=[dict(original=x['original'],canonical=x['canonical'],note=n) for x,n in zip(r['notation_map'],['The source reward is explicitly centered; no zero raw baseline is assumed.','The source empty dividend is zero, and subset sums include the empty set.','The input baseline vector differs from the scalar output baseline.'])]
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Hnet symbols',len(S))
