import sys, os, time
import shutil
import html
import requests
import time

# SERVER="https://aiarchi.art:8005"
SERVER="https://ainterior.space:8005"

if __name__ != "__main__":
    from modules import scripts
    import gradio as gr
    import os, json
    import random
    from modules import script_callbacks
    from modules import sd_models
    import modules
    from modules import scripts, shared, script_callbacks
    from modules.ui_components import FormRow, FormColumn, FormGroup, ToolButton
    from scripts.cryp_gui_func import *


def get_json_content(file_path):
    try:
        with open(file_path, 'rt', encoding="utf-8") as file:
            json_data = json.load(file)
            return json_data
    except Exception as e:
        print(f"A Problem occurred: {str(e)}")


def read_sdxl_styles(json_data):
    # Check that data is a list
    if not isinstance(json_data, list):
        print("Error: input data must be a list")
        return None

    names = []

    # Iterate over each item in the data list
    for item in json_data:
        # Check that the item is a dictionary
        if isinstance(item, dict):
            # Check that 'name' is a key in the dictionary
            if 'name' in item:
                # Append the value of 'name' to the names list
                names.append(item['name'])
    names.sort()
    return names


def getStyles(json_file):
    global stylespath
    global stylebasespath 
    stylebasespath = scripts.basedir()
    json_path = os.path.join(stylebasespath, json_file)
    stylespath = json_path
    json_data = get_json_content(json_path)
    styles = read_sdxl_styles(json_data)
    return styles

def changeStyles(json_file):
    global stylespath
    global stylebasespath 
    json_path = os.path.join(stylebasespath, json_file)
    stylespath = json_path
    json_data = get_json_content(json_path)
    styles = read_sdxl_styles(json_data)
    return styles

def createPositive(style, positive):
    json_data = get_json_content(stylespath)
    ret=''
    try:
        # Check if json_data is a list
        if not isinstance(json_data, list):
            raise ValueError(
                "Invalid JSON data. Expected a list of templates.")
        for val in style:
            print(val)
            for template in json_data:
                # Check if template contains 'name' and 'prompt' fields
                if 'name' not in template or 'prompt' not in template:
                    raise ValueError(
                        "Invalid template. Missing 'name' or 'prompt' field.")

                # Replace {prompt} in the matching template
                if template['name'] == val:
                    ret += template['prompt'].replace(
                        '{prompt}', positive)+','
                    continue


            # If function hasn't returned yet, no matching template was found
            # raise ValueError(f"No template found with name '{val}'.")
        return ret

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def createNegative(style, negative):
    json_data = get_json_content(stylespath)
    try:
        json_negative_prompt=''
        # Check if json_data is a list
        if not isinstance(json_data, list):
            raise ValueError(
                "Invalid JSON data. Expected a list of templates.")
        for val in style:
            for template in json_data:
                # Check if template contains 'name' and 'prompt' fields
                if 'name' not in template or 'prompt' not in template:
                    raise ValueError(
                        "Invalid template. Missing 'name' or 'prompt' field.")

                # Replace {prompt} in the matching template
                if template['name'] == val:
                    json_negative_prompt += template.get('negative_prompt', "")+','
                    continue

            # If function hasn't returned yet, no matching template was found
            # raise ValueError(f"No template found with name '{val}'.")
        if negative:
            negative = f"{json_negative_prompt}, {negative}" if json_negative_prompt else negative
        else:
            negative = json_negative_prompt

        return negative
    except Exception as e:
        print(f"An error occurred: {str(e)}")



if __name__ != "__main__":
    checkpoints_list = sd_models.checkpoints_list.values()

    class Sarshapa(scripts.Script):
        def __init__(self):
            super().__init__()

        styleNames = getStyles('sdxl_styles.json')
        
        def title(self):
            return "模芥Sarshapa"

        def show(self, is_img2img):
            return scripts.AlwaysVisible

        def ui(self, is_img2img):
            with gr.Accordion(f"模芥Sarshapa",open = False) as acc:
                with gr.Blocks() as cryp:
                    time_data = time.time()*1000
                    reg_qrcode = f"""
    <!DOCTYPE html>
    <html>
    <body>
        
        <div width="150px" style="text-align: left;
        color:red;font-size:18px"><img src="{SERVER}/sarshapa/reg_qrcode.png?time={time_data}" width="150px">
        微信扫码使用此插件</div>
    </body>
    </html>"""
                    req_qr = gr.HTML(reg_qrcode)

                enabled = getattr(shared.opts, "enable_sarshapa_styleselector_by_default", False)
            
                with gr.Accordion("起手式", open=True):
                    with FormRow():
                        with FormColumn(min_width=160):
                            is_enabled = gr.Checkbox(
                                value=False, label="启用", info="启用或者禁用起手式")
                        # with FormColumn(elem_id="Randomize Style"):
                        #     randomize = gr.Checkbox(elem_id="Enabled Style",
                        #         value=False, label="", info="启用或者禁用起手式")
                        # with FormColumn(elem_id="Randomize For Each Iteration"):
                        #     randomizeEach = gr.Checkbox(
                        #         value=False, label="每次生图随机", info="每次生图都会使用随机起手式")

                    # with FormRow():
                    #     with FormColumn(min_width=160):
                    #         allstyles = gr.Checkbox(
                    #             value=False, label="按顺序生成所有的起手式", info="要使用所有的起手式生图，最好将生图批次数设置为 " + str(len(self.styleNames)) + " ( 起手式总数)")

                    with FormRow():
                        with FormColumn(min_width=160):
                            btnStyleXL = gr.Button("ADXL起手式")
                        with FormColumn(elem_id="Randomize Style"):
                            btnStyle15 = gr.Button("AD1.5起手式")
                    with FormRow():
                        selected = self.styleNames[0]
                        style = gr.Dropdown(self.styleNames, value=selected, multiselect=True,visible=True, label="选择ADXL起手式")
                        self.styleNames15 = changeStyles('sd1.5_styles.json')
                        selected = self.styleNames15[0]
                        style15 = gr.Dropdown(self.styleNames15, value=selected, multiselect=True,visible=False, label="选择AD1.5起手式")
                        changeStyles('sdxl_styles.json')
                        
                        def handle_StyleXL(input):
                            changeStyles('sdxl_styles.json')
                            return gr.Dropdown.update(visible=True),gr.Dropdown.update(visible=False)
                        def handle_Style15(input):
                            changeStyles('sd1.5_styles.json')
                            return gr.Dropdown.update(visible=False),gr.Dropdown.update(visible=True)
                        btnStyleXL.click(
                            handle_StyleXL,style,[style,style15]
                        )
                        btnStyle15.click(
                            handle_Style15,style15,[style,style15]
                        )
                        # if style_ui_type == "select-list":
                            # style = gr.Dropdown(
                            #     self.styleNames, value='base', multiselect=False, label="选择起手式")
                        # else:
                        #     style = gr.Radio(
                        #         label='起手式列表', choices=self.styleNames, value='base')

            # Ignore the error if the attribute is not present

            return [is_enabled, style, style15]
            # return [is_enabled, randomize, randomizeEach, allstyles, style]

        # def process(self, p, is_enabled, randomize, randomizeEach, allstyles,  style):
        def process(self, p, is_enabled,  style,  style15):
                global stylespath
                if not is_enabled:
                    return

                # if randomize:
                #     style = random.choice(self.styleNames)
                batchCount = len(p.all_prompts)
                if('1.5' in stylespath):
                    # if(batchCount == 1):
                        # for each image in batch
                    for i, prompt in enumerate(p.all_prompts):
                        positivePrompt = createPositive(style15, prompt)
                        p.all_prompts[i] = positivePrompt
                    for i, prompt in enumerate(p.all_negative_prompts):
                        negativePrompt = createNegative(style15, prompt)
                        p.all_negative_prompts[i] = negativePrompt
                    p.extra_generation_params["Sarshapa Style Selector Style"] = style15
                if('sdxl' in stylespath):
                    # if(batchCount == 1):
                        # for each image in batch
                    for i, prompt in enumerate(p.all_prompts):
                        positivePrompt = createPositive(style, prompt)
                        p.all_prompts[i] = positivePrompt
                    for i, prompt in enumerate(p.all_negative_prompts):
                        negativePrompt = createNegative(style, prompt)
                        p.all_negative_prompts[i] = negativePrompt
                    p.extra_generation_params["Sarshapa Style Selector Style"] = style
                # if(batchCount > 1):
                #     styles = {}
                #     for i, prompt in enumerate(p.all_prompts):
                #         if(randomize):
                #             styles[i] = random.choice(self.styleNames)
                #         else:
                #             styles[i] = style
                #         if(allstyles):
                #             styles[i] = self.styleNames[i % len(self.styleNames)]
                #     # for each image in batch
                #     for i, prompt in enumerate(p.all_prompts):
                #         positivePrompt = createPositive(
                #             styles[i] if randomizeEach or allstyles else styles[0], prompt)
                #         p.all_prompts[i] = positivePrompt
                #     for i, prompt in enumerate(p.all_negative_prompts):
                #         negativePrompt = createNegative(
                #             styles[i] if randomizeEach or allstyles else styles[0], prompt)
                #         p.all_negative_prompts[i] = negativePrompt

                p.extra_generation_params["Sarshapa Style Selector Enabled"] = True
                # p.extra_generation_params["Style Selector Randomize"] = randomize

        def after_component(self, component, **kwargs):
            # https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/7456#issuecomment-1414465888 helpfull link
            # Find the text2img textbox component
            if kwargs.get("elem_id") == "txt2img_prompt":  # postive prompt textbox
                self.boxx = component
            # Find the img2img textbox component
            if kwargs.get("elem_id") == "img2img_prompt":  # postive prompt textbox
                self.boxxIMG = component

            # this code below  works aswell, you can send negative prompt text box,provided you change the code a little
            # switch  self.boxx with  self.neg_prompt_boxTXT  and self.boxxIMG with self.neg_prompt_boxIMG

            # if kwargs.get("elem_id") == "txt2img_neg_prompt":
                #self.neg_prompt_boxTXT = component
            # if kwargs.get("elem_id") == "img2img_neg_prompt":
                #self.neg_prompt_boxIMG = component

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
    <img src="{SERVER}/sarshapa/reg_qrcode.png?time={time_data}" width="100%">
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
    <iframe src="{SERVER}/sarshapa/index.html?time={time_data}" width="100%" height="1000">
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
            <img src="{SERVER}/sarshapa/reg_qrcode.png?time={time_data}" width="100%">
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

            <iframe src="{SERVER}/sarshapa/index.html?time={time_data}" width="100%" height="1000">
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

    def on_ui_settings():
        section = ("sarshapastyleselector", "Sarshapa Style Selector")
        # shared.opts.add_option("styles_ui", shared.OptionInfo(
        #     "radio-buttons", "How should Style Names Rendered on UI", gr.Radio, {"choices": ["radio-buttons", "select-list"]}, section=section))

        shared.opts.add_option(
            "enable_sarshapa_styleselector_by_default",
            shared.OptionInfo(
                False,
                "enable Sarshapa Style Selector by default",
                gr.Checkbox,
                section=section
                )
        )
    script_callbacks.on_ui_settings(on_ui_settings)
if __name__ == "__main__":
    pass
