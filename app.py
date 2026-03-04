import streamlit as st
import fitz  # PyMuPDF

# ページの設定
st.set_page_config(page_title="PDF画像変換ツール", layout="centered")

# --- 日本語化のためのカスタムCSS ---
st.markdown("""
    <style>
    /* アップローダー内のテキストを日本語に擬似的に変更 */
    section[data-testid="stFileUploader"] section button [data-testid="stMarkdownContainer"] p {
        font-size: 0;
    }
    section[data-testid="stFileUploader"] section button [data-testid="stMarkdownContainer"] p::before {
        content: "ファイルを選択";
        font-size: 16px;
    }
    section[data-testid="stFileUploader"] [data-testid="stUploadDropzone"] div div span {
        font-size: 0;
    }
    section[data-testid="stFileUploader"] [data-testid="stUploadDropzone"] div div span::before {
        content: "ここにPDFファイルをドラッグ＆ドロップしてください";
        font-size: 16px;
    }
    section[data-testid="stFileUploader"] [data-testid="stUploadDropzone"] div div small {
        font-size: 0;
    }
    section[data-testid="stFileUploader"] [data-testid="stUploadDropzone"] div div small::before {
        content: "1ファイル最大 200MB まで • PDF形式のみ";
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 PDF画像変換ツール")
st.write("PDFファイルをアップロードして、PNG、JPEG、またはTIFF形式に変換します。")

# --- サイドバー設定 ---
st.sidebar.header("変換設定")
out_format = st.sidebar.selectbox(
    "出力形式を選択してください", 
    ["png", "jpg", "tiff"], 
    format_func=lambda x: x.upper()
)
dpi = st.sidebar.slider("解像度 (DPI)", min_value=72, max_value=300, value=150)

# --- メイン機能 ---
# ラベル自体も日本語にします
uploaded_file = st.file_uploader("PDFファイルをアップロード", type="pdf", label_visibility="collapsed")

if uploaded_file is not None:
    pdf_data = uploaded_file.read()
    doc = fitz.open(stream=pdf_data, filetype="pdf")
    
    st.success(f"PDFの読み込みに成功しました（全 {len(doc)} ページ）")
    
    if st.button("変換を開始する"):
        progress_bar = st.progress(0)
        for i in range(len(doc)):
            page = doc.load_page(i)
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
            
            fmt = "jpg" if out_format == "jpg" else out_format
            img_bytes = pix.tobytes(fmt)
            
            st.markdown(f"### {i+1} ページ目")
            st.image(img_bytes, use_container_width=True)
            
            st.download_button(
                label=f"{i+1} ページ目を保存 ({out_format.upper()})",
                data=img_bytes,
                file_name=f"page_{i+1}.{out_format}",
                mime=f"image/{out_format}",
                key=f"btn_{i}"
            )
            progress_bar.progress((i + 1) / len(doc))
        
        st.balloons()
        st.success("すべての変換が完了しました！")
    doc.close()
