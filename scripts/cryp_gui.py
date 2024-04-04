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
            return "模芥Sarshapa"

        def show(self, is_img2img):
            return scripts.AlwaysVisible

        def ui(self, is_img2img):
            with gr.Accordion(f"模芥Sarshapa",open = False) as acc:
                with gr.Blocks() as cryp:
                    # uninstall_btn = gr.Button("卸载加密模块")
                    # operation_output = gr.Textbox(label="操作结果")

                    # # 安装和卸载按钮的点击事件
                    # install_btn.click(
                    #     fn=install_encryption_module, outputs=operation_output
                    # )
                    # uninstall_btn.click(
                    #     fn=uninstall_encryption_module, outputs=operation_output
                    # )
                    time_data = time.time()*1000
                    reg_qrcode = f"""
    <!DOCTYPE html>
    <html>
    <body>
        
        <div width="150px" style="text-align: left;
        color:red;font-size:18px"><img src="https://ainterior.space:8005/sarshapa/reg_qrcode.png?time={time_data}" width="150px">
        微信扫码使用此插件</div>
    </body>
    </html>"""
                    req_qr = gr.HTML(reg_qrcode)

    def on_ui_tabs():
        time_data = time.time()*1000
        username_value, password_value, msg ,html = show_old_login()
        install_msg ,install_result = show_install_result()
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
                            label=f"登录结果     {time_data}",max_lines=1, value=msg, visible=True,id=f"login_result_{time_data}",elem_classes="result_input"
                        )
                        gr.Markdown("模块安装", elem_classes="install_title")
                        if install_result==0:
                            install_btn = gr.Button("安装加密模块")
                            gr.HTML('<button class="lg secondary gradio-button svelte-cmf5ev" style="color:#808080;width:100%" id="component-341466"> 卸载加密模块</button>')
                        else:
                            gr.HTML('<button class="lg secondary gradio-button svelte-cmf5ev" style="color:#808080;width:100%" id="component-341455"> 安装加密模块</button>')
                            uninstall_btn = gr.Button("卸载加密模块")
                        operation_output = gr.Textbox(
                            label=f"加密模块状态     {time_data}",max_lines=1, value=install_msg, visible=True,id=f"login_result_{time_data}",elem_classes="result_input2"
                        )
                        if install_result==0:
                            install_btn.click(fn=install_encryption_module, outputs=operation_output)
                        else:
                            uninstall_btn.click(
                                fn=uninstall_encryption_module, outputs=operation_output
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
.result_input2 span{{
    width: 85px; /* 设置 label 的宽度 */
    overflow: hidden; /* 控制超出部分的显示 */
    white-space: nowrap; /* 禁止文本换行 */
}}
.install_title span{{
    font-size: 16; 
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
            
            login_button.click(
                fn=handle_login,
                inputs=[username_input, password_input],
                outputs=[login_result,users_models],
            )

        return ((cryp, "模芥Sarshapa", "cryp_model"),)

    script_callbacks.on_ui_tabs(on_ui_tabs)
if __name__ == "__main__":
    pass
