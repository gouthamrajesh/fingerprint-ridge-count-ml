import graphviz

def create_block_diagram():
    dot = graphviz.Digraph(comment='Fingerprint Analysis', format='svg')

    dot.node('A', 'Read Image')
    dot.node('B', 'Locate Triradius and Core')
    dot.node('C', 'Preprocess Image')
    dot.node('D', 'Filter Image')
    dot.node('E', 'Convert to Grayscale')
    dot.node('F', 'Thresholding')
    dot.node('G', 'Find Triradius and Core Contours')
    dot.node('H', 'Exclude Triradius Contour')
    dot.node('I', 'Find Core Contour')
    dot.node('J', 'Count Ridges between Triradius and Core')
    dot.node('K', 'Convert Image to Grayscale (if needed)')
    dot.node('L', 'Enhance Ridges using Custom Kernel')
    dot.node('M', 'Create Mask using ROI Contour')
    dot.node('N', 'Apply Mask to Ridge-Enhanced Image')
    dot.node('O', 'Binarize Result')
    dot.node('P', 'Count Ridges')
    dot.node('Q', 'Display Results')

    dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH', 'HI', 'IJ', 'JK',
               'KL', 'LM', 'MN', 'NO', 'OP', 'PQ'])

    dot.render('block_diagram', format='svg', cleanup=True)

if __name__ == "__main__":
    create_block_diagram()
