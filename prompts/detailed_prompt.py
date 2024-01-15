user_prompt_image = """Generate a detailed image creation prompt for DALLE based on a simplified input.
The user provides a basic prompt in square brackets, such as [{text}]. Your task is to elaborate on specific aspects of this input, prompting the user for additional details within curly braces. The resulting comprehensive prompt will be utilized for instructing DALLE in image generation.

Example
Input Prompt: [{input_}]
Elaborated Prompt: Generate an image of a serene scene with a [{prompt1}] donkey peacefully [{prompt2}] on vibrant green grass.
Specify the [{prompt3}] color of its fur and any [{prompt4}]
it may have. Place the donkey in a [{prompt5}] surrounded by
[{prompt6}] like [{prompt7}] and
[{prompt8}]. Enhance the visual by describing the
[{prompt9}] weather and the [{prompt10}] time of day, specifying the
[{prompt11}] that bathes the scene. Add detail with elements like a
[{prompt12}] nearby, and specify any [{prompt13}]
between the donkey and its surroundings, such as [{prompt14}] or [{prompt15}] expressions.
Feel free to include any [{prompt16}] that could contribute to the overall ambiance of the image.

You should always follow the above Example format."""
