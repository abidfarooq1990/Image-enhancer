import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io

# Set page config
st.set_page_config(
    page_title="🎨 Image Quality Enhancer",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .stImage > div > img {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .real-time-indicator {
        background: #e8f5e8;
        border: 2px solid #4caf50;
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class ImageEnhancer:
    def __init__(self):
        self.supported_formats = ['PNG', 'JPEG', 'JPG', 'TIFF', 'TIF']
    
    def validate_image(self, uploaded_file):
        """Validate if the uploaded file is a supported image format"""
        if uploaded_file is None:
            return False, "No file uploaded"
        
        file_extension = uploaded_file.name.split('.')[-1].upper()
        if file_extension not in self.supported_formats:
            return False, f"Unsupported format. Please upload: {', '.join(self.supported_formats)}"
        
        return True, "Valid image file"
    
    def enhance_image(self, image, settings):
        """Apply various enhancement techniques using only PIL"""
        enhanced_image = image.copy()
        
        # 1. Upscaling using PIL
        if settings['scale_factor'] != 1.0:
            enhanced_image = self.upscale_image(enhanced_image, settings['scale_factor'], settings['interpolation'])
        
        # 2. Apply brightness
        if settings['brightness'] != 1.0:
            enhancer = ImageEnhance.Brightness(enhanced_image)
            enhanced_image = enhancer.enhance(settings['brightness'])
        
        # 3. Apply contrast
        if settings['contrast'] != 1.0:
            enhancer = ImageEnhance.Contrast(enhanced_image)
            enhanced_image = enhancer.enhance(settings['contrast'])
        
        # 4. Apply saturation
        if settings['saturation'] != 1.0:
            enhancer = ImageEnhance.Color(enhanced_image)
            enhanced_image = enhancer.enhance(settings['saturation'])
        
        # 5. Apply sharpening
        if settings['sharpness'] != 1.0:
            enhancer = ImageEnhance.Sharpness(enhanced_image)
            enhanced_image = enhancer.enhance(settings['sharpness'])
        
        # 6. Apply noise reduction (using PIL filters)
        if settings['noise_reduction'] > 0:
            enhanced_image = self.apply_noise_reduction(enhanced_image, settings['noise_reduction'])
        
        return enhanced_image
    
    def upscale_image(self, image, scale_factor, interpolation_method):
        """Upscale image using PIL only"""
        # Map interpolation methods to PIL constants
        interpolation_map = {
            'Bicubic': Image.BICUBIC,
            'Bilinear': Image.BILINEAR,
            'Lanczos': Image.LANCZOS,
            'Nearest': Image.NEAREST
        }
        
        interpolation = interpolation_map.get(interpolation_method, Image.BICUBIC)
        
        # Calculate new size
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        
        return image.resize((new_width, new_height), interpolation)
    
    def apply_noise_reduction(self, image, noise_reduction_factor):
        """Apply noise reduction using PIL filters only"""
        if noise_reduction_factor <= 0.3:
            # Light smoothing
            radius = noise_reduction_factor * 2
            return image.filter(ImageFilter.GaussianBlur(radius=radius))
        elif noise_reduction_factor <= 0.6:
            # Medium smoothing
            return image.filter(ImageFilter.SMOOTH_MORE)
        else:
            # Heavy smoothing
            smoothed = image.filter(ImageFilter.SMOOTH_MORE)
            radius = (noise_reduction_factor - 0.6) * 3
            return smoothed.filter(ImageFilter.GaussianBlur(radius=radius))
    
    def get_image_stats(self, image):
        """Get image statistics"""
        img_array = np.array(image)
        return {
            'width': image.width,
            'height': image.height,
            'channels': len(img_array.shape) if len(img_array.shape) > 2 else 1,
            'mean_brightness': np.mean(img_array),
            'std_brightness': np.std(img_array),
            'file_size_mb': len(image.tobytes()) / (1024 * 1024)
        }

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎨 Image Quality Enhancer</h1>
        <p style="text-align: center; color: white; margin: 0;">
            Minimal Dependencies Version - Works on All Platforms!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Success message
    st.success("✅ **Minimal Version Loaded Successfully!** - Only using PIL + NumPy")
    
    # Initialize enhancer
    if 'enhancer' not in st.session_state:
        st.session_state.enhancer = ImageEnhancer()
    
    # File upload
    st.subheader("📁 Upload Your Image")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'tiff', 'tif'],
        help="Upload JPEG, PNG, or TIFF images"
    )
    
    if uploaded_file is None:
        st.info("👆 Please upload an image file to get started!")
        st.markdown("""
        ### 📋 Features (Minimal Version):
        - **Real-time preview**: See changes instantly
        - **Image upscaling**: 1x to 4x resolution increase
        - **Basic enhancements**: Brightness, contrast, saturation, sharpness
        - **Noise reduction**: Gaussian blur and smoothing filters
        - **Download results**: Save your enhanced images
        - **Zero dependency issues**: Uses only PIL and NumPy
        """)
        return
    
    # Validate file
    is_valid, message = st.session_state.enhancer.validate_image(uploaded_file)
    if not is_valid:
        st.error(f"❌ {message}")
        return
    
    # Load image
    try:
        original_image = Image.open(uploaded_file)
        if original_image.mode == 'RGBA':
            original_image = original_image.convert('RGB')
        
        st.session_state.original_image = original_image
        st.success(f"✅ Image loaded: {original_image.width}×{original_image.height} pixels")
    except Exception as e:
        st.error(f"❌ Error loading image: {str(e)}")
        return
    
    # Real-time enhancement indicator
    st.markdown("""
    <div class="real-time-indicator">
        🔄 <strong>Real-time Enhancement Active</strong> - Adjust sliders to see instant changes!
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for controls and preview
    control_col, preview_col = st.columns([1, 2])
    
    with control_col:
        st.header("🛠️ Enhancement Settings")
        
        # Scaling Options
        st.subheader("🔍 Scaling Options")
        scale_factor = st.slider(
            "Scale Factor",
            min_value=1.0,
            max_value=4.0,
            value=2.0,
            step=0.1,
            help="Increase image resolution",
            key="scale_factor"
        )
        
        interpolation_method = st.selectbox(
            "Interpolation Method",
            ['Bicubic', 'Bilinear', 'Lanczos', 'Nearest'],
            index=0,
            help="Algorithm used for upscaling",
            key="interpolation"
        )
        
        # Enhancement Controls
        st.subheader("✨ Enhancement Controls")
        brightness = st.slider(
            "Brightness",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Adjust image brightness",
            key="brightness"
        )
        
        contrast = st.slider(
            "Contrast",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Adjust image contrast",
            key="contrast"
        )
        
        saturation = st.slider(
            "Saturation",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Adjust color saturation",
            key="saturation"
        )
        
        sharpness = st.slider(
            "Sharpness",
            min_value=0.5,
            max_value=3.0,
            value=1.0,
            step=0.1,
            help="Enhance image sharpness",
            key="sharpness"
        )
        
        # Noise Reduction
        st.subheader("🎛️ Noise Reduction")
        noise_reduction = st.slider(
            "Noise Reduction",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Reduce image noise (using Gaussian blur)",
            key="noise_reduction"
        )
        
        # Reset button
        if st.button("🔄 Reset All Settings", type="secondary"):
            st.session_state.scale_factor = 2.0
            st.session_state.brightness = 1.0
            st.session_state.contrast = 1.0
            st.session_state.saturation = 1.0
            st.session_state.sharpness = 1.0
            st.session_state.noise_reduction = 0.0
            st.rerun()
    
    with preview_col:
        # Enhancement settings dictionary
        settings = {
            'scale_factor': scale_factor,
            'interpolation': interpolation_method,
            'brightness': brightness,
            'contrast': contrast,
            'saturation': saturation,
            'sharpness': sharpness,
            'noise_reduction': noise_reduction
        }
        
        # Real-time enhancement
        try:
            with st.spinner("🔄 Applying enhancements..."):
                enhanced_image = st.session_state.enhancer.enhance_image(original_image, settings)
            
            # Display images in tabs
            tab1, tab2 = st.tabs(["🔍 Comparison View", "📊 Statistics"])
            
            with tab1:
                # Side-by-side comparison
                img_col1, img_col2 = st.columns(2)
                
                with img_col1:
                    st.subheader("📷 Original")
                    st.image(original_image, use_container_width=True)
                    st.caption(f"Size: {original_image.width}×{original_image.height}")
                
                with img_col2:
                    st.subheader("✨ Enhanced")
                    st.image(enhanced_image, use_container_width=True)
                    st.caption(f"Size: {enhanced_image.width}×{enhanced_image.height}")
                
                # Download button
                img_buffer = io.BytesIO()
                enhanced_image.save(img_buffer, format='PNG', quality=95)
                img_buffer.seek(0)
                
                st.download_button(
                    label="💾 Download Enhanced Image",
                    data=img_buffer.getvalue(),
                    file_name=f"enhanced_{uploaded_file.name.split('.')[0]}.png",
                    mime="image/png",
                    type="primary",
                    use_container_width=True
                )
            
            with tab2:
                # Get statistics
                original_stats = st.session_state.enhancer.get_image_stats(original_image)
                enhanced_stats = st.session_state.enhancer.get_image_stats(enhanced_image)
                
                # Display metrics
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                
                with stat_col1:
                    st.metric(
                        "🔍 Resolution",
                        f"{enhanced_stats['width']} × {enhanced_stats['height']}",
                        f"+{enhanced_stats['width'] - original_stats['width']} × +{enhanced_stats['height'] - original_stats['height']}"
                    )
                
                with stat_col2:
                    st.metric(
                        "💾 File Size",
                        f"{enhanced_stats['file_size_mb']:.2f} MB",
                        f"{enhanced_stats['file_size_mb'] - original_stats['file_size_mb']:+.2f} MB"
                    )
                
                with stat_col3:
                    st.metric(
                        "🔆 Brightness",
                        f"{enhanced_stats['mean_brightness']:.1f}",
                        f"{enhanced_stats['mean_brightness'] - original_stats['mean_brightness']:+.1f}"
                    )
                
                # Detailed comparison table
                st.subheader("📋 Detailed Comparison")
                comparison_data = {
                    "Metric": ["Width", "Height", "Total Pixels", "File Size (MB)", "Mean Brightness"],
                    "Original": [
                        f"{original_stats['width']}px",
                        f"{original_stats['height']}px", 
                        f"{original_stats['width'] * original_stats['height']:,}",
                        f"{original_stats['file_size_mb']:.2f}",
                        f"{original_stats['mean_brightness']:.1f}"
                    ],
                    "Enhanced": [
                        f"{enhanced_stats['width']}px",
                        f"{enhanced_stats['height']}px",
                        f"{enhanced_stats['width'] * enhanced_stats['height']:,}",
                        f"{enhanced_stats['file_size_mb']:.2f}",
                        f"{enhanced_stats['mean_brightness']:.1f}"
                    ]
                }
                
                st.table(comparison_data)
                
                # Enhancement summary
                resolution_increase = (enhanced_stats['width'] * enhanced_stats['height']) / (original_stats['width'] * original_stats['height'])
                st.success(f"🎉 **Enhancement Complete**: {resolution_increase:.1f}x total pixel increase!")
        
        except Exception as e:
            st.error(f"❌ Enhancement failed: {str(e)}")
            st.info("💡 Try adjusting the settings or uploading a different image")
            st.write("Debug info:", str(e))

    # Info section
    with st.expander("ℹ️ About This Minimal Version"):
        st.markdown("""
        ### 🔧 Technical Details:
        - **Dependencies**: Only PIL (Pillow) and NumPy
        - **Upscaling**: PIL's built-in interpolation algorithms
        - **Enhancements**: PIL's ImageEnhance module
        - **Noise Reduction**: Gaussian blur and smoothing filters
        - **Compatibility**: Works on all Streamlit Cloud deployments
        
        ### 🎯 Features Available:
        - ✅ **Image upscaling** with multiple interpolation methods
        - ✅ **Brightness and contrast** adjustment
        - ✅ **Color saturation** control
        - ✅ **Sharpness enhancement**
        - ✅ **Basic noise reduction**
        - ✅ **Real-time preview**
        - ✅ **Download enhanced images**
        - ✅ **Live statistics**
        
        ### 💡 Why This Version Works:
        This version uses only the most basic, well-supported libraries that are 
        guaranteed to be available on Streamlit Cloud, avoiding complex dependencies
        that can cause import errors.
        """)

if __name__ == "__main__":
    main()
