import sys, os, time
import shutil
import html
import requests
import time

if __name__ != "__main__":
    from modules import scripts
    import gradio as gr
    import os, json
    from modules import script_callbacks
    from modules import sd_models
    import modules
    from scripts.cryp_gui_func import *





if __name__ != "__main__":
    checkpoints_list = sd_models.checkpoints_list.values()

    class Png2SqlJson(scripts.Script):
        def __init__(self):
            super().__init__()

        def title(self):
            return "ad3.0 tool"

        def show(self, is_img2img):
            return scripts.AlwaysVisible

        def ui(self, is_img2img):
            with gr.Blocks() as cryp:
                gr.Markdown("模芥Sarshapa")

                install_btn = gr.Button("安装加密模块")
                uninstall_btn = gr.Button("卸载加密模块")
                operation_output = gr.Textbox(label="操作结果")

                # 安装和卸载按钮的点击事件
                install_btn.click(
                    fn=install_encryption_module, outputs=operation_output
                )
                uninstall_btn.click(
                    fn=uninstall_encryption_module, outputs=operation_output
                )

    def on_ui_tabs():
        time_data = time.time()*1000
        username_value, password_value, msg ,html = show_old_login()
        with gr.Blocks() as cryp:

            with gr.TabItem("登录", id="login"):
                with gr.Row():
                    with gr.Column(scale=1):
                        username_input = gr.Textbox(
                            label=f"用户ID   {time_data}",max_lines=1, value=username_value,id=f"username_input_{time_data}",show_copy_button=True,elem_classes="username_input"
                        )
                        password_input = gr.Textbox(
                            label=f"密钥    {time_data}",max_lines=1, value=password_value, type="password",id=f"password_input_{time_data}",show_copy_button=True,elem_classes="password_input"
                        )
                        login_button = gr.Button("登录")
                        login_result = gr.Textbox(
                            label=f"登录结果    {time_data}",max_lines=1, value=msg, visible=True,id=f"login_result_{time_data}",elem_classes="result_input"
                        )
                        reg_qrcode = f"""
<!DOCTYPE html>
<html>
<style>
.username_input span{{
    width: 40px; /* 设置 label 的宽度 */
    overflow: hidden; /* 控制超出部分的显示 */
    white-space: nowrap; /* 禁止文本换行 */
}}
.password_input span{{
    width: 28px; /* 设置 label 的宽度 */
    overflow: hidden; /* 控制超出部分的显示 */
    white-space: nowrap; /* 禁止文本换行 */
}}
.result_input span{{
    width: 55px; /* 设置 label 的宽度 */
    overflow: hidden; /* 控制超出部分的显示 */
    white-space: nowrap; /* 禁止文本换行 */
}}
</style>
<body>
    <img src="https://ainterior.space:8005/sarshapa/reg_qrcode.png?time={time_data}" width="100%">
    <div width="100%" style="text-align: center;
    color:red;font-size:18px">微信扫码注册获取密钥</div>
</body>
</html>"""
                        req_qr = gr.HTML(reg_qrcode)

                    with gr.Column(scale=7):
                        
                        iframe_html=""
                        if not html=="" :
                            iframe_html= html
                        else :
                            iframe_html = f"""
<!DOCTYPE html>
<html>
<body>
    <!-- 使用 iframe 标签嵌入外部HTML页面 -->
    <iframe src="https://ainterior.space:8005/sarshapa/index.html?time={time_data}" width="100%" height="1000">
        <p>您的浏览器不支持iframe标签。</p>
    </iframe>
</body>
</html>"""
                        users_models = gr.HTML(iframe_html)
            with gr.TabItem("下载模型", id="download_model"):
                with gr.Row():
                    with gr.Column(scale=1):

                        
                        html = f"""
        <!DOCTYPE html>
        <html>
        <body>
            <img src="https://ainterior.space:8005/sarshapa/reg_qrcode.png?time={time_data}" width="100%">
            <div width="100%" style="text-align: center;
            color:red;font-size:18px">微信扫码注册购买模型</div>
        </body>
        </html>"""
                        reg_qr = gr.HTML(html)
                    with gr.Column(scale=8):

                        
                        html = f"""
        <!DOCTYPE html>
        <html>
        <body>
            <!-- 使用 iframe 标签嵌入外部HTML页面 -->

            <iframe src="https://ainterior.space:8005/sarshapa/index.html?time={time_data}" width="100%" height="1000">
                <p>您的浏览器不支持iframe标签。</p>
            </iframe>
        </body>
        </html>"""
                        product_show = gr.HTML(html)
            with gr.TabItem("解密模块安装和卸载", id="encryption"):
                with gr.Row():
                    with gr.Column(scale=1):
                        
                        install_btn = gr.Button("安装加密模块")
                        uninstall_btn = gr.Button("卸载加密模块")
                        operation_output = gr.Textbox(label="操作结果")
                        html = f"""
<!DOCTYPE html>
<html>
<body>
    <img src="https://ainterior.space:8005/sarshapa/reg_qrcode.png?time={time_data}" width="100%">
    <div width="100%" style="text-align: center;
    color:red;font-size:18px">微信扫码注册获取密钥</div>
</body>
</html>"""
                        reg_qr = gr.HTML(html)
                    with gr.Column(scale=8):
                        
                        html_css = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Image in Container</title>
<style>
    html, body {
        margin: 0;
        padding: 0;
        /* 移除默认的边距和内边距 */
    }
    .image-container {
        width: 1280px; /* 容器宽度，假设比图片小 */
        height: 720px; /* 容器高度 */
        overflow: hidden;
    }
    
    .image-container img {
        width: 100%;
        height: 100%;
        object-fit: contain; /* 保证图片按比例完整展示 */
    }
</style>
</head>
<body>
'''
                        html_css = html_css + f'''
<div class="image-container">
    <img src="https://ainterior.space:8005/sarshapa/guid.jpg?time={time_data}" alt="">
</div>

</body>
</html>
'''
                        guid = gr.HTML(html_css)






            login_button.click(
                fn=handle_login,
                inputs=[username_input, password_input],
                outputs=[login_result,users_models],
            )
            install_btn.click(fn=install_encryption_module, outputs=operation_output)
            uninstall_btn.click(
                fn=uninstall_encryption_module, outputs=operation_output
            )
        return ((cryp, "模芥Sarshapa", "cryp_model"),)

    script_callbacks.on_ui_tabs(on_ui_tabs)
if __name__ == "__main__":
    pass
