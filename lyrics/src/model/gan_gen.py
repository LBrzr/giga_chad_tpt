import tensorflow as tf
import numpy as np

# Define hyperparameters
batch_size = 128
epochs = 100
latent_dim = 100
num_tokens = 10000
max_sequence_length = 20
embedding_dim = 64
lstm_units = 128
learning_rate = 0.001

# Load and preprocess text data
text = open('corpus.txt').read()
text = text.lower()
tokenizer = tf.keras.preprocessing.text.Tokenizer(
    num_words=num_tokens, oov_token='<OOV>')
tokenizer.fit_on_texts([text])
sequences = tokenizer.texts_to_sequences([text])[0]
sequences = [seq for seq in sequences if len(seq) <= max_sequence_length]
sequences = np.array(sequences)
dataset = tf.data.Dataset.from_tensor_slices(sequences)
dataset = dataset.shuffle(buffer_size=10000)
dataset = dataset.batch(batch_size, drop_remainder=True)

# Define generator model
generator = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(latent_dim,)),
    tf.keras.layers.Dense(embedding_dim),
    tf.keras.layers.Dense(max_sequence_length * lstm_units),
    tf.keras.layers.Reshape((max_sequence_length, lstm_units)),
    tf.keras.layers.LSTM(lstm_units, return_sequences=True),
    tf.keras.layers.LSTM(lstm_units, return_sequences=True),
    tf.keras.layers.TimeDistributed(
        tf.keras.layers.Dense(num_tokens, activation='softmax'))
])

# Define discriminator model
discriminator = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(max_sequence_length, num_tokens)),
    tf.keras.layers.LSTM(lstm_units, return_sequences=True),
    tf.keras.layers.LSTM(lstm_units),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Define loss functions and optimizers
cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
generator_optimizer = tf.keras.optimizers.Adam(learning_rate)
discriminator_optimizer = tf.keras.optimizers.Adam(learning_rate)

# Define training loop


@tf.function
def train_step(real_sequences):
    # Generate random noise vectors
    noise = tf.random.normal([batch_size, latent_dim])

    # Generate fake sequences using generator
    with tf.GradientTape() as gen_tape:
        generated_sequences = generator(noise, training=True)

        # Evaluate discriminator on real and fake sequences
        real_scores = discriminator(real_sequences, training=True)
        fake_scores = discriminator(generated_sequences, training=True)

        # Compute generator loss and gradients
        gen_loss = cross_entropy(tf.ones_like(fake_scores), fake_scores)
        gen_gradients = gen_tape.gradient(
            gen_loss, generator.trainable_variables)

    # Update generator
    generator_optimizer.apply_gradients(
        zip(gen_gradients, generator.trainable_variables))

    # Train discriminator on real sequences
    with tf.GradientTape() as disc_tape:
        real_scores = discriminator(real_sequences, training=True)
        real_loss = cross_entropy(tf.ones_like(real_scores), real_scores)
        real_gradients = disc_tape.gradient(
            real_loss, discriminator.trainable_variables)

    # Train discriminator on fake sequences
    with tf.GradientTape() as disc_tape:
        fake_scores = discriminator(generated_sequences, training=True)
        fake_loss = cross_entropy(tf.zeros_like(fake_scores), fake_scores)
        fake_gradients = disc_tape.gradient(
            fake_loss, discriminator.trainable_variables)

    # Update discriminator
    discriminator_gradients = [real_grad + fake_grad for real_grad,
                               fake_grad in zip(real_gradients, fake_gradients)]
    discriminator_optimizer.apply_gradients(
        zip(discriminator_gradients, discriminator.trainable_variables))


# Train model# Training the generator
for epoch in range(epochs):
    print("Epoch:", epoch+1)
    for batch in range(num_batches):
        # Get a random batch of input sequences
        idx = np.random.randint(0, num_sequences-batch_size)
        input_batch = sequences[idx:idx+batch_size, :-1]
        target_batch = np.expand_dims(
            sequences[idx:idx+batch_size, -1], axis=-1)

        # Generate noise for the generator
        noise = np.random.normal(0, 1, size=(batch_size, noise_dim))

        # Train the generator to fool the discriminator
        gan_loss, gen_loss = train_generator(noise, target_batch)

        # Train the discriminator on real and generated data
        dis_loss = train_discriminator(input_batch, target_batch, noise)

    print(
        f"Generator loss: {gen_loss:.4f} | Discriminator loss: {dis_loss:.4f}")

    # Generate some text samples
    for _ in range(5):
        generate_text(generator, tokenizer, max_sequence_len, temperature=0.5)
