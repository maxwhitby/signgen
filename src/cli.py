"""
Command-line interface for Sign Generator
"""

import argparse
import sys
from pathlib import Path
from .sign_generator import SignGenerator
from .logger import get_logger


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate parametric signs for 3D printing"
    )

    # Required arguments
    parser.add_argument("text", help="Text to display on the sign")

    # Dimension arguments
    parser.add_argument(
        "--width", type=float, default=100,
        help="Sign width in mm (default: 100)"
    )
    parser.add_argument(
        "--height", type=float, default=25,
        help="Sign height in mm (default: 25)"
    )

    # Text arguments
    parser.add_argument(
        "--font", default="Arial",
        help="Font family (default: Arial)"
    )
    parser.add_argument(
        "--font-size", type=float,
        help="Font size in mm (auto-calculated if not specified)"
    )
    parser.add_argument(
        "--heaviness", type=int, default=50,
        help="Text heaviness 0-100 (default: 50)"
    )

    # Layer arguments
    parser.add_argument(
        "--bottom-thickness", type=float, default=1.0,
        help="Bottom layer thickness in mm (default: 1.0)"
    )
    parser.add_argument(
        "--top-thickness", type=float, default=1.0,
        help="Top layer thickness in mm (default: 1.0)"
    )

    # Output arguments
    parser.add_argument(
        "--output-dir", default="output",
        help="Output directory for STL files (default: output)"
    )

    # Other options
    parser.add_argument(
        "--no-auto-size", action="store_true",
        help="Disable automatic font sizing"
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    # Initialize logger
    logger = get_logger(args.debug)

    # Create generator
    generator = SignGenerator(output_dir=args.output_dir, debug=args.debug)

    try:
        # Generate sign
        logger.info(f"Generating sign: '{args.text}'")

        models = generator.generate_sign(
            text=args.text,
            width=args.width,
            height=args.height,
            font_family=args.font,
            font_size=args.font_size if not args.no_auto_size else args.font_size,
            heaviness=args.heaviness,
            bottom_thickness=args.bottom_thickness,
            top_thickness=args.top_thickness,
            auto_size=not args.no_auto_size and args.font_size is None,
            validate=True
        )

        # Export STL files
        metadata = {
            'heaviness': args.heaviness,
            'font': args.font,
            'width': args.width,
            'height': args.height
        }

        created_files = generator.export_stl(
            models=models,
            base_filename=args.text,
            metadata=metadata
        )

        # Report success
        print(f"\n✅ Successfully generated {len(created_files)} files:")
        for file in created_files:
            print(f"  - {Path(file).name}")
        print(f"\nFiles saved to: {generator.output_dir}")

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()