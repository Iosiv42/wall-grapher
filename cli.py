import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Wall Grapher",
        description="Steganography on images. Program isn't strong cryptography"
    )

    parser.add_argument("input_image")

    parser.add_argument("-e", "--encode", action="store_true")
    parser.add_argument("-o", "--output_image")

    parser.add_argument("-d", "--decode", action="store_true")
    parser.add_argument("-i", "--input_data")

    # parser.add_argument("-p", "--mask_pattern") TODO

    args = parser.parse_args()

    assert (args.encode or args.output_image is not None or args.input_data is not None) != args.decode

    if args.encode:
        from encode import encode
        
        with open(args.input_data) as f:
            data = f.read()
        encode(args.input_image, args.output_image, data)
    else:
        from decode import decode
        print(decode(args.input_image))
