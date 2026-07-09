import streamlit as st
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="3D 智能模型生成器", layout="centered")
st.title("文字生成 360° 可旋转 3D 模型")
st.write("试试输入：'生成一个3D爱心'，或者 '生成一个半径1米高2米的圆柱'！")

user_input = st.text_input("请输入您的需求")

if st.button("一键生成 3D 模型"):
    if user_input:
        with st.spinner("正在计算3D几何体..."):

            shape_type = "box"
            l, w, h = 2.0, 2.0, 2.0
            radius = 0.0

            if "爱心" in user_input or "心形" in user_input:
                shape_type = "heart"
            elif "圆柱" in user_input or "柱体" in user_input:
                shape_type = "cylinder"
            elif "球" in user_input:
                shape_type = "sphere"

            if shape_type in ["box"]:
                match_length = re.search(r'长[\s:]*(\d+\.?\d*)', user_input)
                match_width = re.search(r'宽[\s:]*(\d+\.?\d*)', user_input)
                match_height = re.search(r'高[\s:]*(\d+\.?\d*)', user_input)
                l = float(match_length.group(1)) if match_length else l
                w = float(match_width.group(1)) if match_width else w
                h = float(match_height.group(1)) if match_height else h
                desc = f"长 {l}米 宽 {w}米 高 {h}米 的立方体"

            elif shape_type == "cylinder":
                match_radius = re.search(r'半径[\s:]*(\d+\.?\d*)', user_input)
                match_height = re.search(r'高[\s:]*(\d+\.?\d*)', user_input)
                radius = float(match_radius.group(1)) if match_radius else 1.0
                h = float(match_height.group(1)) if match_height else 2.0
                desc = f"半径 {radius}米 高 {h}米 的圆柱体"

            elif shape_type == "sphere":
                match_radius = re.search(r'半径[\s:]*(\d+\.?\d*)', user_input)
                radius = float(match_radius.group(1)) if match_radius else 1.5
                desc = f"半径 {radius}米 的球体"

            elif shape_type == "heart":
                desc = "3D模型"

            st.success(f"正在渲染：{desc}")
            if shape_type == "heart":

                threejs_geometry = """
                // 1. 创建左边圆球
                const sphereGeo = new THREE.SphereGeometry(0.5, 32, 16);
                const material = new THREE.MeshStandardMaterial({ color: 0xff0000, emissive: 0x880000, roughness: 0.3, metalness: 0.1 });

                const leftSphere = new THREE.Mesh(sphereGeo, material);
                leftSphere.position.set(-0.5, 0.2, 0);
                scene.add(leftSphere);

                // 2. 创建右边圆球
                const rightSphere = new THREE.Mesh(sphereGeo, material);
                rightSphere.position.set(0.5, 0.2, 0);
                scene.add(rightSphere);

                // 3. 创建下方的倒三角（心尖部分）
                const coneGeo = new THREE.ConeGeometry(0.7, 1.2, 32);
                const cone = new THREE.Mesh(coneGeo, material);
                cone.position.set(0, -0.3, 0);
                cone.rotation.z = Math.PI / 2; 
                scene.add(cone);

                // 4. 整体加入场景
                const heartGroup = new THREE.Group();
                heartGroup.add(leftSphere);
                heartGroup.add(rightSphere);
                heartGroup.add(cone);
                heartGroup.scale.set(1.5, 1.5, 1.5);
                scene.add(heartGroup);
                """
            else:
                threejs_geometry = f"""
                let geometry;
                if ("{shape_type}" === "box") {{
                    geometry = new THREE.BoxGeometry({l}, {h}, {w});
                }} else if ("{shape_type}" === "cylinder") {{
                    geometry = new THREE.CylinderGeometry({radius}, {radius}, {h}, 32);
                }} else if ("{shape_type}" === "sphere") {{
                    geometry = new THREE.SphereGeometry({radius}, 32, 32);
                }}
                const material = new THREE.MeshStandardMaterial({{ color: 0x3498db, roughness: 0.3, metalness: 0.1 }});
                const cube = new THREE.Mesh(geometry, material);
                scene.add(cube);
                """

            html_content = f"""
            <!DOCTYPE html><html><head><meta charset="utf-8"><title>3D 渲染</title>
            <style>body{{margin:0;overflow:hidden;background:#1a1a1a;}}
            #info{{position:absolute;top:15px;left:15px;color:#fff;font-family:sans-serif;background:rgba(0,0,0,0.6);padding:5px 12px;border-radius:20px;pointer-events:none;}}</style>
            <script type="importmap">{{"imports":{{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}}}</script>
            <script type="module">
            import * as THREE from 'three'; import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
            const scene = new THREE.Scene(); scene.background = new THREE.Color(0x1a1a1a);
            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(5, 4, 5);
            const renderer = new THREE.WebGLRenderer({{ antialias: true }}); renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);
            const controls = new OrbitControls(camera, renderer.domElement); controls.enableDamping = true;
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6); scene.add(ambientLight);
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.8); dirLight.position.set(5, 10, 7); scene.add(dirLight);
            {threejs_geometry}
            window.addEventListener('resize', () => {{ camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight); }});
            function animate() {{ requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }} animate();
            </script></body></html>
            """
            components.html(html_content, height=600)
    else:
        st.warning("请输入描述，比如：'生成一个3D爱心'")
