import torch
import nodes
import comfy.utils

class SC_EmptyLatentImageAutoCascade1B:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "width": ("INT", {"default": 1024, "min": 512, "max": 4096, "step": 32}),
            "height": ("INT", {"default": 1024, "min": 512, "max": 4096, "step": 32}),
            "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096})
        }}
    RETURN_TYPES = ("LATENT", "LATENT")
    RETURN_NAMES = ("stage_c", "stage_b")
    FUNCTION = "generate"

    CATEGORY = "latent/stable_cascade"

    def ensure_divisible_by_32(self, value):
        if value % 32 != 0:  # Check if number is not divisible by 32
            value = (value // 32) * 32 + 32  # Round up to the nearest multiple of 32
        return value

    PRESET_LATENT_SIZES = [
        (61, 16), (60, 16), (59, 17), (58, 17), (57, 17), (56, 18), (55, 18), (54, 18), 
        (53, 19), (52, 19), (51, 19), (50, 20), (49, 20), (48, 20), (48, 21), (47, 21), 
        (46, 21), (46, 22), (45, 22), (44, 22), (44, 23), (43, 23), (42, 23), (42, 24), 
        (41, 24), (40, 24), (40, 25), (39, 25), (39, 26), (38, 26), (37, 26), (37, 27), 
        (36, 27), (36, 28), (35, 28), (35, 29), (34, 29), (34, 30), (33, 30), (33, 31), 
        (32, 31), (32, 32), (31, 32), (30, 33), (30, 34), (29, 34), (29, 35), (28, 35), 
        (28, 36), (27, 36), (27, 37), (26, 37), (26, 38), (26, 39), (25, 39), (25, 40), 
        (24, 40), (24, 41), (24, 42), (23, 42), (23, 43), (23, 44), (22, 44), (22, 45), 
        (22, 46), (21, 46), (21, 47), (21, 48), (20, 48), (20, 49), (20, 50), (20, 51), 
        (19, 51), (19, 52), (19, 53), (18, 53), (18, 54), (18, 55), (18, 56), (17, 56), 
        (17, 57), (17, 58), (17, 59), (17, 60), (16, 60), (16, 61)
    ]

    multiplied_sizes = [(int(x * 0.75), int(y * 0.75)) for x, y in PRESET_LATENT_SIZES]

    def generate(self, width, height, batch_size=1):

        # Calculate aspect ratio of the input dimensions
        input_aspect_ratio = width / height

        # Find the nearest preset latent size based on aspect ratio
        best_match = min(self.multiplied_sizes, key=lambda size: abs((size[0] / size[1]) - input_aspect_ratio))

        # Use the dimensions of the best matching latent size
        c_width = best_match[0]
        c_height = best_match[1]
        width_compression = (width // c_width)
        height_compression = (height // c_height)
        compression_mean = ((width_compression + height_compression) / 2)

        print(f"Stage C latent dimensions set to: {c_width}x{c_height} Compression was: {width_compression}x{height_compression}({compression_mean} mean)")

        # Calculate new width and height for stage B latent images based on compression factor
        b_width = int(c_width * compression_mean)
        b_height = int(c_height * compression_mean)
        b_width_even = self.ensure_divisible_by_32(b_width)
        b_height_even = self.ensure_divisible_by_32(b_height)

        print(f"Stage B latent dimensions set to: {b_width_even // 4}x{b_height_even // 4}")

        c_latent = torch.zeros([batch_size, 16, c_height, c_width])
        b_latent = torch.zeros([batch_size, 4, b_height_even // 4, b_width_even // 4])
        
        return ({
            "samples": c_latent,
        }, {
            "samples": b_latent,
        })


NODE_CLASS_MAPPINGS = {
    "SC_EmptyLatentImageAutoCascade1B": SC_EmptyLatentImageAutoCascade1B,
}
