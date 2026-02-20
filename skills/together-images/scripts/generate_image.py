#!/usr/bin/env python3
"""
Together AI Image Generation — Generate, Save, and Edit Images (v2 SDK)

Text-to-image generation with FLUX models, including base64 saving,
multiple variations, and image-to-image editing.

Usage:
    python generate_image.py

Requires:
    pip install together
    export TOGETHER_API_KEY=your_key
"""

import base64
from together import Together

client = Together()


def generate_image_url(
    prompt: str,
    model: str = "black-forest-labs/FLUX.1-schnell",
    width: int = 1024,
    height: int = 1024,
    steps: int = 4,
    n: int = 1,
    seed: int | None = None,
) -> list[str]:
    """Generate image(s) and return URL(s)."""
    kwargs = dict(
        model=model,
        prompt=prompt,
        width=width,
        height=height,
        steps=steps,
        n=n,
    )
    if seed is not None:
        kwargs["seed"] = seed

    response = client.images.generate(**kwargs)
    urls = [img.url for img in response.data]
    for i, url in enumerate(urls):
        print(f"  Image {i}: {url}")
    return urls


def generate_and_save(
    prompt: str,
    output_path: str = "output.png",
    model: str = "black-forest-labs/FLUX.1-schnell",
    width: int = 1024,
    height: int = 1024,
    steps: int = 4,
    seed: int | None = None,
) -> str:
    """Generate an image and save it locally via base64."""
    kwargs = dict(
        model=model,
        prompt=prompt,
        width=width,
        height=height,
        steps=steps,
        n=1,
        response_format="base64",
    )
    if seed is not None:
        kwargs["seed"] = seed

    response = client.images.generate(**kwargs)
    image_data = base64.b64decode(response.data[0].b64_json)

    with open(output_path, "wb") as f:
        f.write(image_data)

    print(f"  Saved to {output_path} ({len(image_data)} bytes)")
    return output_path


def edit_image(
    prompt: str,
    image_url: str,
    model: str = "black-forest-labs/FLUX.1-kontext-pro",
    width: int = 1024,
    height: int = 1024,
) -> str:
    """Edit an existing image using a text prompt (image-to-image)."""
    response = client.images.generate(
        model=model,
        prompt=prompt,
        image_url=image_url,
        width=width,
        height=height,
    )
    url = response.data[0].url
    print(f"  Edited image: {url}")
    return url


if __name__ == "__main__":
    # --- Example 1: Generate with URL response ---
    print("Generating image (URL):")
    urls = generate_image_url(
        prompt="A serene mountain landscape at sunset, digital art",
        steps=4,
    )

    # --- Example 2: Generate and save locally ---
    print("\nGenerating image (saved to file):")
    generate_and_save(
        prompt="A futuristic city skyline with flying cars",
        output_path="city.png",
        steps=4,
    )

    # --- Example 3: Multiple variations ---
    print("\nGenerating 3 variations:")
    generate_image_url(
        prompt="A cute robot reading a book",
        n=3,
        steps=4,
    )

    # --- Example 4: Reproducible with seed ---
    print("\nReproducible generation (seed=42):")
    generate_image_url(
        prompt="Abstract geometric pattern in blue and gold",
        seed=42,
        steps=4,
    )

    # --- Example 5: Image editing (requires a source image URL) ---
    # print("\nEditing image:")
    # edit_image(
    #     prompt="Transform this into a watercolor painting",
    #     image_url="https://example.com/source.jpg",
    # )
