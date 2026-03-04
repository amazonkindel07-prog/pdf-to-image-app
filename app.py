import streamlit as st
import fitz  # PyMuPDF

# ページの設定
st.set_page_config(page_title="PDF画像変換ツール", layout="centered")

st.title("📄 PDF画像変換ツール")
st.write("PDFファイルをアップロードして、PNG、JPEG、またはTIFF形式に変換します。")

# --- サイドバー設定（日本語） ---
st.sidebar.header("変換設定")
out_format = st.sidebar.selectbox(
    "出力形式を選択してください", 
    ["png", "jpg", "tiff"], 
    format_func=lambda x: x.upper()
)
dpi = st.sidebar.slider("解像度 (DPI) - 数値が高いほど高画質になります", min_value=72, max_value=300, value=150)

# --- メイン機能 ---
uploaded_file = st.file_uploader("PDFファイルを選択（またはドラッグ＆ドロップ）", type="pdf")

if uploaded_file is not None:
    # PDFを読み込む
    pdf_data = uploaded_file.read()
    doc = fitz.open(stream=pdf_data, filetype="pdf")
    
    st.success(f"PDFの読み込みに成功しました（全 {len(doc)} ページ）")
    
    # 変換実行ボタン
    if st.button("変換を開始する"):
        progress_bar = st.progress(0)
        
        for i in range(len(doc)):
            page = doc.load_page(i)
            
            # 高画質レンダリング設定
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
            
            # 内部的な形式指定（jpegはjpgとして処理）
            fmt = "jpg" if out_format == "jpg" else out_format
            img_bytes = pix.tobytes(fmt)
            
            # プレビュー表示
            st.markdown(f"### {i+1} ページ目")
            st.image(img_bytes, use_container_width=True)
            
            # ダウンロードボタン
            st.download_button(
                label=f"{i+1} ページ目を保存 ({out_format.upper()})",
                data=img_bytes,
                file_name=f"page_{i+1}.{out_format}",
                mime=f"image/{out_format}",
                key=f"btn_{i}"
            )
            
            # 進捗バーの更新
            progress_bar.progress((i + 1) / len(doc))
        
        st.balloons() # 完了時にお祝いの演出
        st.success("すべてのページの変換が完了しました！")
    
    doc.close()