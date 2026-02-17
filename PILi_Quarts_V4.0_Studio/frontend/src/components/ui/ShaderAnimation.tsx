
import { useEffect, useRef } from "react"
import * as THREE from "three"

export function ShaderAnimation() {
    const containerRef = useRef<HTMLDivElement>(null)
    const sceneRef = useRef<{
        camera: THREE.Camera
        scene: THREE.Scene
        renderer: THREE.WebGLRenderer
        uniforms: any
        animationId: number
    } | null>(null)

    useEffect(() => {
        if (!containerRef.current) return

        const container = containerRef.current

        // Vertex shader
        const vertexShader = `
      void main() {
        gl_Position = vec4( position, 1.0 );
      }
    `

        // Fragment shader
        const fragmentShader = `
      precision highp float;
      uniform vec2 uResolution;
      uniform float uTime;

      void main(void) {
        vec2 res = uResolution;
        vec2 uv = (gl_FragCoord.xy * 2.0 - res.xy) / min(res.x, res.y);
        float t = uTime * 0.05;
        float lw = 0.002;
        
        // Evitar mod() y usar fract() para mayor estabilidad en algunos drivers
        float animBase = 5.0 - length(uv) + (fract((uv.x + uv.y) * 5.0) * 0.2);

        float r = 0.0;
        float g = 0.0;
        float b = 0.0;

        for(int i = 0; i < 5; i++) {
          float fi = float(i);
          float iOffset = fi * 0.01;
          
          // Acceso explícito a componentes para evitar dyn_index_vec3_int
          r += (lw * fi * fi) / (0.001 + abs(fract(t + iOffset) * 5.0 - animBase));
          g += (lw * fi * fi) / (0.001 + abs(fract(t + 0.01 + iOffset) * 5.0 - animBase));
          b += (lw * fi * fi) / (0.001 + abs(fract(t + 0.02 + iOffset) * 5.0 - animBase));
        }
        
        gl_FragColor = vec4(clamp(vec3(r, g, b), 0.0, 1.0), 1.0);
      }
    `

        // Initialize Three.js scene
        const camera = new THREE.Camera()
        camera.position.z = 1

        const scene = new THREE.Scene()
        const geometry = new THREE.PlaneGeometry(2, 2)

        const uniforms = {
            uTime: { value: 1.0 },
            uResolution: { value: new THREE.Vector2() },
        }

        const material = new THREE.ShaderMaterial({
            uniforms: uniforms,
            vertexShader: vertexShader,
            fragmentShader: fragmentShader,
        })

        const mesh = new THREE.Mesh(geometry, material)
        scene.add(mesh)

        const renderer = new THREE.WebGLRenderer({ antialias: true })
        renderer.setPixelRatio(window.devicePixelRatio)

        container.appendChild(renderer.domElement)

        // Handle window resize
        const onWindowResize = () => {
            if (!container) return
            const width = container.clientWidth
            const height = container.clientHeight
            renderer.setSize(width, height)
            uniforms.uResolution.value.x = renderer.domElement.width
            uniforms.uResolution.value.y = renderer.domElement.height
        }

        // Initial resize
        onWindowResize()
        window.addEventListener("resize", onWindowResize, false)

        // Animation loop
        const animate = () => {
            const animationId = requestAnimationFrame(animate)
            uniforms.uTime.value += 0.05
            renderer.render(scene, camera)

            if (sceneRef.current) {
                sceneRef.current.animationId = animationId
            }
        }

        // Store scene references for cleanup
        sceneRef.current = {
            camera,
            scene,
            renderer,
            uniforms,
            animationId: 0,
        }

        // Start animation
        animate()

        // Cleanup function
        return () => {
            window.removeEventListener("resize", onWindowResize)

            if (sceneRef.current) {
                cancelAnimationFrame(sceneRef.current.animationId)

                if (container && sceneRef.current.renderer.domElement) {
                    container.removeChild(sceneRef.current.renderer.domElement)
                }

                sceneRef.current.renderer.dispose()
                geometry.dispose()
                material.dispose()
            }
        }
    }, [])

    return (
        <div
            ref={containerRef}
            className="absolute inset-0 w-full h-full pointer-events-none"
            style={{
                background: "#000",
                overflow: "hidden",
                zIndex: 0
            }}
        />
    )
}
