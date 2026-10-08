"""Build dist/pixel-id-maker.html: inlines fonts, QR library, background and the pixel-fade engine into one offline HTML file."""
import base64, re
import os
ROOT=os.path.dirname(os.path.abspath(__file__))+'/'
A=ROOT+'assets/'
old=open(ROOT+'src/pixel-fade-tool.html').read()

# --- pixel fade engine, extracted from the tool ---
g0=old.index("function geometry(W, H) {"); g1=old.index("function render()")
geo=old[g0:g1].strip()
a=old.index("  const g = grid = geometry(W,H);"); b=old.index("  out.width = W; out.height = H;")
body=old[a:b].replace("const g = grid = geometry(W,H);","const g = geometry(W,H);")
body=re.sub(r"  \$\('info'\)\.textContent = .*\n","",body)
assert "$('info')" not in body and 'dims' not in body, 'engine extraction leaked UI code'
engine = ("function fadeEngine(photo, bg, P, W, H, seed) {\n  const $ = id => ({ value: P[id] });\n  "
          + geo.replace("\n","\n  ") + "\n" + body +
          "  const out = document.createElement('canvas'); out.width = W; out.height = H;\n  out.getContext('2d').putImageData(id, 0, 0);\n  return out;\n}\n")

# --- fonts ---
def face(fam,pkg,fn,wt):
    d=base64.b64encode(open(A+'fonts/'+fn,'rb').read()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;src:url(data:font/woff2;base64,{d}) format('woff2');}}\n"
css=(face('Pixelify Sans','pixelify-sans','pixelify-sans-latin-700-normal.woff2',700)+
     face('Silkscreen','silkscreen','silkscreen-latin-400-normal.woff2',400)+
     face('Silkscreen','silkscreen','silkscreen-latin-700-normal.woff2',700)+
     face('Chakra Petch','chakra-petch','chakra-petch-latin-700-normal.woff2',700)+
     face('Space Grotesk','space-grotesk','space-grotesk-latin-400-normal.woff2',400)+
     face('Space Grotesk','space-grotesk','space-grotesk-latin-700-normal.woff2',700))

U=A+'fonts/'
def otf(fam,fn,wt):
    d=base64.b64encode(open(U+fn,'rb').read()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;src:url(data:font/otf;base64,{d}) format('opentype');}}\n"
css+=otf('IntraNet','IntraNet-Regular.otf',400)+otf('IntraNet','IntraNet-Bold.otf',700)+otf('IntraNet Outline','IntraNet-Outline.otf',400)+otf('IntraNet Italic','IntraNet-Italic.otf',400)
qr=open(A+'vendor/qrcode.js').read()
assert '</script' not in qr
bg=base64.b64encode(open(A+'pixel-bg.png','rb').read()).decode()
html=open(ROOT+'src/id-maker.html').read()
for k,v in [('__FONTCSS__',css),('__QR__',qr),('__ENGINE__',engine),('__BG__','data:image/png;base64,'+bg)]:
    html=html.replace(k,v)
open(ROOT+'dist/pixel-id-maker.html','w').write(html)
print(len(html)//1024,'KB')
