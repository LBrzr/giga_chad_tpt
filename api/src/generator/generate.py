from generator.one_step import OneStep


def genarate(generator: OneStep, seed: str, length: int) -> str:
    result = [seed]
    for n in range(100):
        next_char, states = generator.generate_one_step(
            next_char, states=states)
        result.append(next_char)
    return ''.join(result)
