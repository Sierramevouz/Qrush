from rl_discriminator import DiscriminatorAgent

original = [{'name': 'h', 'qubits': [0]}, {'name': 'h', 'qubits': [0]}]
rewrited = [{'name': 'h', 'qubits': [0]}]

disc = DiscriminatorAgent()
reward = disc.evaluate(original, rewrited)
print(f"Discriminator reward: {reward}")
