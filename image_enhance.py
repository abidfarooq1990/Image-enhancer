import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
from scipy import ndimage
from skimage import restoration, filters
import matplotlib.pyplot as plt

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
    
    .enhancement-stats {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .metric-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
        """Apply various enhancement techniques to the image"""
        # Convert PIL to numpy array
        img_array = np.array(image)
        
        # 1. Upscaling with different interpolation methods
        if settings['scale_factor'] != 1.0:
            img_array = self.upscale_image(img_array, settings['scale_factor'], settings['interpolation'])
        
        # 2. Convert to PIL for easier manipulation
        enhanced_image = Image.fromarray(img_array.astype('uint8'))
        
        # 3. Apply brightness
        if settings['brightness'] != 1.0:
            enhancer = ImageEnhance.Brightness(enhanced_image)
            enhanced_image = enhancer.enhance(settings['brightness'])
        
        # 4. Apply contrast
        if settings['contrast'] != 1.0:
            enhancer = ImageEnhance.Contrast(enhanced_image)
            enhanced_image = enhancer.enhance(settings['contrast'])
        
        # 5. Apply saturation
        if settings['saturation'] != 1.0:
            enhancer = ImageEnhance.Color(enhanced_image)
            enhanced_image = enhancer.enhance(settings['saturation'])
        
        # 6. Apply sharpening
        if settings['sharpness'] > 1.0:
            enhanced_image = self.apply_sharpening(enhanced_image, settings['sharpness'])
        
        # 7. Apply noise reduction
        if settings['noise_reduction'] > 0:
            enhanced_image = self.apply_noise_reduction(enhanced_image, settings['noise_reduction'])
        
        return enhanced_image
    
    def upscale_image(self, img_array, scale_factor, interpolation_method):
        """Upscale image using different interpolation methods"""
        height, width = img_array.shape[:2]
        new_height = int(height * scale_factor)
        new_width = int(width * scale_factor)
        
        interpolation_map = {
            'Bicubic': cv2.INTER_CUBIC,
            'Bilinear': cv2.INTER_LINEAR,
            'Lanczos': cv2.INTER_LANCZOS4,
            'Nearest': cv2.INTER_NEAREST
        }
        
        interpolation = interpolation_map.get(interpolation_method, cv2.INTER_CUBIC)
        
        if len(img_array.shape) == 3:
            upscaled = cv2.resize(img_array, (new_width, new_height), interpolation=interpolation)
        else:
            upscaled = cv2.resize(img_array, (new_width, new_height), interpolation=interpolation)
        
        return upscaled
    
    def apply_sharpening(self, image, sharpness_factor):
        """Apply unsharp masking for sharpening"""
        # Convert to numpy array
        img_array = np.array(image)
        
        # Create gaussian blur
        blurred = ndimage.gaussian_filter(img_array.astype(float), sigma=1.0)
        
        # Calculate unsharp mask
        sharpened = img_array + (sharpness_factor - 1.0) * (img_array - blurred)
        
        # Clip values to valid range
        sharpened = np.clip(sharpened, 0, 255)
        
        return Image.fromarray(sharpened.astype('uint8'))
    
    def apply_noise_reduction(self, image, noise_reduction_factor):
        """Apply noise reduction using various filters"""
        img_array = np.array(image)
        
        if noise_reduction_factor <= 0.3:
            # Light denoising - Gaussian blur
            sigma = noise_reduction_factor * 2
            denoised = ndimage.gaussian_filter(img_array.astype(float), sigma=sigma)
        elif noise_reduction_factor <= 0.6:
            # Medium denoising - Bilateral filter
            if len(img_array.shape) == 3:
                denoised = cv2.bilateralFilter(img_array, 9, 75, 75)
            else:
                denoised = cv2.bilateralFilter(img_array, 9, 75, 75)
        else:
            # Heavy denoising - Non-local means
            if len(img_array.shape) == 3:
                denoised = cv2.fastNlMeansDenoisingColored(img_array, None, 10, 10, 7, 21)
            else:
                denoised = cv2.fastNlMeansDenoising(img_array, None, 10, 7, 21)
        
        return Image.fromarray(denoised.astype('uint8'))
    
    def get_image_stats(self, image):
        """Get image statistics"""
        img_array = np.array(image)
        return {
            'width': image.width,
            'height': image.height,
            'channels': len(img_array.shape),
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
            Real-time image enhancement with live preview
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize enhancer
    if 'enhancer' not in st.session_state:
        st.session_state.enhancer = ImageEnhancer()
    
    # File upload - moved to main area for better visibility
    st.subheader("📁 Upload Your Image")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'tiff', 'tif'],
        help="Upload JPEG, PNG, or TIFF images"
    )
    
    if uploaded_file is None:
        st.info("👆 Please upload an image file to get started!")
        st.markdown("""
        ### 📋 Features:
        - **Real-time preview**: See changes instantly as you adjust sliders
        - **Multiple formats**: JPEG, PNG, TIFF support
        - **Advanced algorithms**: Professional-grade enhancement
        - **Live statistics**: Monitor image metrics in real-time
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
        
        # Store original image in session state
        st.session_state.original_image = original_image
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
        
        # Enhancement settings with keys for real-time updates
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
        
        st.subheader("🎛️ Noise Reduction")
        noise_reduction = st.slider(
            "Noise Reduction",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Reduce image noise",
            key="noise_reduction"
        )
        
        # Reset button
        if st.button("🔄 Reset All Settings", type="secondary"):
            # Reset all sliders to default values
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
            
            # Display images in tabs for better organization
            tab1, tab2 = st.tabs(["🔍 Comparison View", "📊 Statistics"])
            
            with tab1:
                # Create sub-columns for side-by-side comparison
                img_col1, img_col2 = st.columns(2)
                
                with img_col1:
                    st.subheader("📷 Original")
                    st.image(original_image, use_container_width=True)
                
                with img_col2:
                    st.subheader("✨ Enhanced")
                    st.image(enhanced_image, use_container_width=True)
                
                # Download button
                img_buffer = io.BytesIO()
                enhanced_image.save(img_buffer, format='PNG')
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
                # Get statistics for both images
                original_stats = st.session_state.enhancer.get_image_stats(original_image)
                enhanced_stats = st.session_state.enhancer.get_image_stats(enhanced_image)
                
                # Display statistics in columns
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                
                with stat_col1:
                    st.metric(
                        "🔍 Resolution",
                        f"{enhanced_stats['width']} × {enhanced_stats['height']}",
                        f"{enhanced_stats['width'] - original_stats['width']} × {enhanced_stats['height'] - original_stats['height']}"
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
                
                # Detailed comparison
                st.subheader("📈 Detailed Comparison")
                
                comparison_data = {
                    "Metric": ["Width", "Height", "Total Pixels", "File Size (MB)", "Mean Brightness", "Brightness Std"],
                    "Original": [
                        original_stats['width'],
                        original_stats['height'],
                        original_stats['width'] * original_stats['height'],
                        f"{original_stats['file_size_mb']:.2f}",
                        f"{original_stats['mean_brightness']:.1f}",
                        f"{original_stats['std_brightness']:.1f}"
                    ],
                    "Enhanced": [
                        enhanced_stats['width'],
                        enhanced_stats['height'],
                        enhanced_stats['width'] * enhanced_stats['height'],
                        f"{enhanced_stats['file_size_mb']:.2f}",
                        f"{enhanced_stats['mean_brightness']:.1f}",
                        f"{enhanced_stats['std_brightness']:.1f}"
                    ]
                }
                
                st.table(comparison_data)
                
                # Enhancement summary
                resolution_increase = (enhanced_stats['width'] * enhanced_stats['height']) / (original_stats['width'] * original_stats['height'])
                st.success(f"🎉 **Enhancement Summary**: {resolution_increase:.1f}x resolution increase with {enhanced_stats['width']}×{enhanced_stats['height']} final dimensions")
        
        except Exception as e:
            st.error(f"❌ Enhancement failed: {str(e)}")
            st.info("💡 Try adjusting the settings or uploading a different image")
    
    # Additional information
    with st.expander("ℹ️ About Real-time Enhancement"):
        st.markdown("""
        ### 🔄 Real-time Processing:
        - **Instant Preview**: See changes immediately as you adjust sliders
        - **No Button Required**: Processing happens automatically
        - **Live Statistics**: Metrics update in real-time
        - **Optimized Performance**: Efficient algorithms for smooth interaction
        
        ### 🎛️ Enhancement Controls:
        - **Scale Factor**: Increase resolution up to 4x
        - **Interpolation**: Choose algorithm for upscaling quality
        - **Brightness/Contrast**: Adjust image tone and dynamic range
        - **Saturation**: Control color intensity
        - **Sharpness**: Apply unsharp masking for detail enhancement
        - **Noise Reduction**: Remove unwanted noise and artifacts
        
        ### 💡 Tips for Best Results:
        - Start with small adjustments and build up
        - Use different interpolation methods for different image types
        - Combine multiple enhancements for optimal results
        - Monitor statistics to avoid over-processing
        """)

if __name__ == "__main__":
    main()