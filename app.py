import streamlit as st
import fitz  # PyMuPDF

# ページの設定
st.set_page_config(page_title="PDF画像変換ツール", layout="centered")

# --- CSSで標準の英語パーツを非表示にし、デザインを整える ---
st.markdown("""
    <style>
    /* 標準のアップローダー内の英語テキストを非表示にする */
    div[data-testid="stFileUploader"] section div div {
        display: none;
    }
    /* アップロードエリアに日本語のメッセージを表示 */
    div[data-testid="stFileUploader"] section::before {
        content: "ここにPDFファイルをドラッグ＆ドロップしてください";
        display: block;
        text-align: center;
        color: #555;
        padding: 20px;
    }
    /* ファイル選択ボタンを日本語にする */
    div[data-testid="stFileUploader"] section button::before {
        content: "ファイルを選択する";
        visibility: visible;
    }
    div[data-testid="stFileUploader"] section button {
        font-size: 0;
        width: 100%;
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
# 日本語のラベルを指定
uploaded_file = st.file_uploader("PDFファイル（最大200MB）", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    st.success(f"読み込み完了：全 {len(doc)} ページ")
    
    if st.button("変換を開始する"):
        progress_bar = st.progress(0)
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
            img_bytes = pix.tobytes("jpg" if out_format == "jpg" else out_format)
            
            st.markdown(f"### {i+1} ページ目")
            st.image(img_bytes, use_container_width=True)
            st.download_button(f"{i+1} ページ目を保存", img_bytes, f"page_{i+1}.{out_format}")
            
            progress_bar.progress((i + 1) / len(doc))
        st.balloons()
    doc.close()
