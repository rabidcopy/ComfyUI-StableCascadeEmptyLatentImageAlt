import torch

class SC_EmptyLatentImageAutoCascade768Advanced:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "width": ("INT", {"default": 1024, "min": 512, "max": 4096, "step": 32}),
            "height": ("INT", {"default": 1024, "min": 512, "max": 4096, "step": 32}),
            "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
            "offset": ("INT", {"default": 0, "min": -16, "max": 16})
        }}
    RETURN_TYPES = ("LATENT", "LATENT")
    RETURN_NAMES = ("stage_c", "stage_b")
    FUNCTION = "generate"

    CATEGORY = "latent/stable_cascade"

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

    def generate(self, width, height, offset, batch_size=1):

        # Calculate aspect ratio of the input dimensions
        input_aspect_ratio = width / height

        # Find the nearest preset latent size based on aspect ratio
        best_match = min(self.multiplied_sizes, key=lambda size: abs((size[0] / size[1]) - input_aspect_ratio))

        # Use the dimensions of the best matching latent size
        c_width = best_match[0] + offset
        c_height = best_match[1] + offset

        print(f"Stage C latent dimensions set to: {c_width}x{c_height}")

        b_width = c_width * 8
        b_height = c_height * 8

        print(f"Stage B latent dimensions set to: {b_width}x{b_height}")

        c_latent = torch.zeros([batch_size, 16, c_height, c_width])
        b_latent = torch.zeros([batch_size, 4, b_height, b_width])
        
        return ({
            "samples": c_latent,
        }, {
            "samples": b_latent,
        })


NODE_CLASS_MAPPINGS = {
    "SC_EmptyLatentImageAutoCascade768Advanced": SC_EmptyLatentImageAutoCascade768Advanced,
}
