#!/usr/bin/env python3
"""
Test script to debug PDF export functionality
"""

def test_reportlab_import():
    """Test if reportlab can be imported and basic functionality works"""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        print("✅ All reportlab imports successful")
        return True
    except ImportError as e:
        print(f"❌ ImportError: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

def test_pdf_creation():
    """Test creating a simple PDF"""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        import tempfile
        import os
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        
        # Create PDF document
        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Add content
        story.append(Paragraph("Test PDF Export", styles['Title']))
        story.append(Paragraph("This is a test PDF to verify reportlab functionality.", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        temp_file.close()
        
        # Check if file was created
        if os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 0:
            print(f"✅ PDF created successfully: {temp_file.name}")
            print(f"   File size: {os.path.getsize(temp_file.name)} bytes")
            # Clean up
            os.unlink(temp_file.name)
            return True
        else:
            print("❌ PDF file was not created or is empty")
            return False
            
    except Exception as e:
        print(f"❌ PDF creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing PDF Export Dependencies...")
    print("=" * 50)
    
    # Test imports
    if test_reportlab_import():
        print("\nTesting PDF creation...")
        test_pdf_creation()
    else:
        print("\n❌ Cannot proceed with PDF creation test due to import errors")
        print("\nTo fix this, run:")
        print("pip install reportlab")
