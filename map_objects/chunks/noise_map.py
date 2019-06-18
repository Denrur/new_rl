import noise


def make_noise_map(x, y, size):
    max_noise = float('-inf')
    min_noise = float('inf')
    scale = 10
    octaves = 5
    persistance = 0.3
    lactunarity = 1.1
    height_map = dict()
    for j in range(x, x + size):
        for k in range(y, y + size):
            noise_value = noise.snoise2(j / scale, k / scale,
                                        octaves,
                                        persistance,
                                        lactunarity)

            if noise_value > max_noise:
                max_noise = noise_value
            elif noise_value < min_noise:
                min_noise = noise_value
            height_map[(j, k)] = noise_value

    return height_map, max_noise, min_noise
