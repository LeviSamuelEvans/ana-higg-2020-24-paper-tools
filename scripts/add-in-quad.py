import sys

def combine_uncertainties(uncertainty1, uncertainty2):
    """Combine two uncertainties given in percentage in quadrature.
    """
    # convert percentage to fraction
    u1 = uncertainty1 / 100
    u2 = uncertainty2 / 100

    # combined uncertainty in quadrature
    combined_uncertainty = (u1**2 + u2**2)**0.5

    combined_uncertainty_percentage = combined_uncertainty * 100

    return combined_uncertainty_percentage

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python combine_uncertainties.py <uncertainty1> <uncertainty2>")
        sys.exit(1)

    try:
        uncertainty1 = float(sys.argv[1])
        uncertainty2 = float(sys.argv[2])
    except ValueError:
        print("Please provide valid numbers for uncertainties.")
        sys.exit(1)

    combined = combine_uncertainties(uncertainty1, uncertainty2)
    print(f"The combined uncertainty is {combined:.2f}%")