import streamlit as st
import open3d as o3d
import re
import numpy as np
st.set_page_config(page_title="AI 3D 立体生成器", layout="wide")
st.title("输入文字，秒出 360° 可旋转 3D 立体模型")
st.write("输入长、宽、高，甚至轴的半径，系统将实时生成三维立体模型并在网页中展示。")
user_input = st.text_input("请输入您的需求 (例如: 生成一个长 5米 宽 3米 高 2米的立方体，或者半径 1米的圆柱)")

if st.button("一键生成 3D 模型"):
    if user_input:
        with st.spinner("正在空间中构建 3D 立体模型..."):
            match_length = re.search(r'长[\s:]*(\d+\.?\d*)', user_input)
            match_width = re.search(r'宽[\s:]*(\d+\.?\d*)', user_input)
            match_height = re.search(r'高[\s:]*(\d+\.?\d*)', user_input)
            match_radius = re.search(r'半径[\s:]*(\d+\.?\d*)', user_input)

            if match_radius:
                r = float(match_radius.group(1))
                h = float(match_height.group(1)) if match_height else 2.0
                mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=r, height=h)
                st.success(f"成功生成：半径 {r}米，高 {h}米的圆柱体！")
            elif match_length and match_width and match_height:
                l = float(match_length.group(1))
                w = float(match_width.group(1))
                h = float(match_height.group(1))
                mesh = o3d.geometry.TriangleMesh.create_box(width=l, height=h, depth=w)
                st.success(f"成功生成：长 {l}米，宽 {w}米，高 {h}米的立方体！")
            else:
                st.warning("未识别到具体尺寸，默认生成一个 2x2x2 的展示方块。")
                mesh = o3d.geometry.TriangleMesh.create_box(2, 2, 2)
            mesh.compute_vertex_normals()
            mesh.paint_uniform_color([0.2, 0.6, 0.8])

            with open("temp_model.html", "w") as f:
                o3d.io.write_triangle_mesh("temp.obj", mesh)
                f.write(o3d.visualization.VisualizerWithEditing().capture_screen_float_buffer()) 

            st.components.v1.html(open("temp_model.html", 'r').read(), height=600, scrolling=True)
    else:
        st.warning("请先输入关于长宽高的描述。")
