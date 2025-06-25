# Image-enhancer
Tool for image enhancement
# 🎨 Image Quality Enhancer

A professional-grade image enhancement web application built with Streamlit, featuring real-time preview and advanced processing algorithms.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **🔄 Real-time Enhancement**: See changes instantly as you adjust parameters
- **📈 Advanced Upscaling**: Multiple interpolation algorithms (Bicubic, Bilinear, Lanczos, Nearest)
- **🎛️ Professional Controls**: Brightness, contrast, saturation, sharpness adjustment
- **🎯 Noise Reduction**: Gaussian blur, bilateral filtering, and non-local means denoising
- **📊 Live Statistics**: Real-time image metrics and comparison data
- **💾 Multiple Formats**: Support for PNG, JPEG, TIFF image formats
- **🖼️ Side-by-Side Comparison**: Visual before/after comparison
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/image-quality-enhancer.git
   cd image-quality-enhancer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run image_enhance.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL manually

## 📦 Dependencies

Create a `requirements.txt` file with these dependencies:

```
streamlit>=1.28.0
opencv-python>=4.8.0
numpy>=1.24.0
Pillow>=10.0.0
scipy>=1.11.0
scikit-image>=0.21.0
matplotlib>=3.7.0
```

## 🎯 Usage

### Basic Workflow

1. **Upload Image**: Click "Choose an image file" and select your image
2. **Adjust Settings**: Use the sliders in the left panel to enhance your image
3. **Real-time Preview**: Watch changes appear instantly in the preview
4. **Compare Results**: Switch between "Comparison View" and "Statistics" tabs
5. **Download**: Click "Download Enhanced Image" to save your result

### Enhancement Controls

#### 🔍 Scaling Options
- **Scale Factor**: Increase resolution from 1x to 4x
- **Interpolation Method**: Choose upscaling algorithm
  - *Bicubic*: Best for photographs (default)
  - *Bilinear*: Faster, good for general use
  - *Lanczos*: Sharp results, good for detailed images
  - *Nearest*: Fastest, preserves sharp edges

#### ✨ Enhancement Controls
- **Brightness**: Adjust overall image brightness (0.5-2.0x)
- **Contrast**: Control dynamic range (0.5-2.0x)
- **Saturation**: Modify color intensity (0.0-2.0x)
- **Sharpness**: Apply unsharp masking (0.5-3.0x)

#### 🎛️ Noise Reduction
- **Light (0.0-0.3)**: Gaussian blur for subtle smoothing
- **Medium (0.3-0.6)**: Bilateral filter preserving edges
- **Heavy (0.6-1.0)**: Non-local means for maximum noise removal

## 📊 Technical Details

### Algorithms Used

- **Upscaling**: OpenCV interpolation methods
- **Sharpening**: Unsharp masking with Gaussian blur
- **Noise Reduction**: 
  - Gaussian filtering
  - Bilateral filtering
  - Non-local means denoising
- **Color Enhancement**: PIL ImageEnhance modules

### Supported Formats

| Format | Extensions | Notes |
|--------|------------|-------|
| JPEG   | .jpg, .jpeg | Lossy compression |
| PNG    | .png | Lossless, transparency support |
| TIFF   | .tiff, .tif | Uncompressed, high quality |

### Performance Considerations

- **Memory Usage**: Large images may require significant RAM
- **Processing Time**: Higher scale factors and noise reduction increase processing time
- **Real-time Updates**: Optimized for smooth slider interaction

## 🛠️ Development

### Project Structure

```
image-quality-enhancer/
│
├── image_enhance.py          # Main application file
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── .gitignore               # Git ignore file
```

### Key Classes

- **`ImageEnhancer`**: Core enhancement functionality
  - `validate_image()`: File format validation
  - `enhance_image()`: Main enhancement pipeline
  - `upscale_image()`: Resolution scaling
  - `apply_sharpening()`: Unsharp masking
  - `apply_noise_reduction()`: Noise filtering
  - `get_image_stats()`: Image statistics

### Customization

To add new enhancement features:

1. Add new parameters to the `settings` dictionary
2. Implement the enhancement in `ImageEnhancer.enhance_image()`
3. Add UI controls in the Streamlit interface
4. Update statistics collection if needed

## 🐛 Troubleshooting

### Common Issues

**"No module named 'cv2'"**
```bash
pip install opencv-python
```

**"Image format not supported"**
- Ensure your image is PNG, JPEG, or TIFF
- Check file extension matches actual format

**"Memory error with large images"**
- Reduce scale factor
- Use smaller input images
- Close other applications to free RAM

**"Slow performance"**
- Reduce noise reduction settings
- Use lower scale factors
- Try different interpolation methods

### Performance Tips

- Start with scale factor 2.0 or lower for large images
- Use Bilinear interpolation for faster processing
- Apply noise reduction sparingly on high-resolution images
- Reset settings if the app becomes unresponsive

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/image-quality-enhancer.git

# Install in development mode
pip install -e .

# Run with auto-reload
streamlit run image_enhance.py --server.runOnSave true
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web app framework
- **OpenCV** - For computer vision algorithms
- **scikit-image** - For advanced image processing
- **PIL/Pillow** - For image manipulation
- **NumPy & SciPy** - For numerical computing

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/yourusername/image-quality-enhancer/issues)
- 💡 **Feature Requests**: [Discussion board](https://github.com/yourusername/image-quality-enhancer/discussions)
- 📧 **Email**: your.email@example.com

## 🔄 Version History

- **v1.0.0** - Initial release with core enhancement features
- **v1.1.0** - Added real-time preview and statistics
- **v1.2.0** - Enhanced noise reduction algorithms

---

**Made with ❤️ and Python**
