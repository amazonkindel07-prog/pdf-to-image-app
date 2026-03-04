import streamlit as st
import fitz  # PyMuPDF

# ページの設定
st.set_page_config(page_title="PDF画像変換ツール", layout="centered")

# --- シンプルなデザイン調整 ---
st.markdown("""
    <style>
    /* アップロードエリアを少し目立たせる */
    [data-testid="stFileUploader"] {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 PDF画像変換ツール")
st.write("PDFをアップロードして、画像（PNG/JPG/TIFF）に変換します。")

# --- サイドバー設定 ---
st.sidebar.header("変換設定")
out_format = st.sidebar.selectbox("出力形式", ["png", "jpg", "tiff"], format_func=lambda x: x.upper())
dpi = st.sidebar.slider("解像度 (DPI)", 72, 300, 150)

# --- メイン機能 ---
st.markdown("### 1. PDFファイルを準備してください")
# label引数に日本語の説明をしっかり入れることで、英語の補助テキストが気にならないようにします
uploaded_file = st.file_uploader(
    "ここにPDFファイルをドラッグ＆ドロップ、または「Browse files」から選択してください", 
    type="pdf",
    help="最大200MBまでのPDFに対応しています"
)

if uploaded_file:
    st.markdown("---")
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    st.success(f"✅ 読み込み完了（全 {len(doc)} ページ）")
    
    st.markdown("### 2. 変換を実行する")
    if st.button("画像を生成してダウンロードボタンを表示する", type="primary", use_container_width=True):
        progress_bar = st.progress(0)
        for i in range(len(doc)):
            page = doc.load_page(i)
            # 解像度設定
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
            
            fmt = "jpg" if out_format == "jpg" else out_format
            img_bytes = pix.tobytes(fmt)
            
            # プレビューとボタン
            with st.container():
                st.markdown(f"#### 📄 {i+1} ページ目")
                st.image(img_bytes)
                st.download_button(
                    label=f"Page {i+1} を保存する", 
                    data=img_bytes, 
                    file_name=f"page_{i+1}.{out_format}",
                    mime=f"image/{out_format}",
                    key=f"dl_{i}"
                )
            
            progress_bar.progress((i + 1) / len(doc))
        st.balloons()
    doc.close()
