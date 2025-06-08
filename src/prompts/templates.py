COMMAND_GENERATION_PROMPT = """Task: Generate a bash command based on the following structured input.
Requirements:
1. Use standard bash commands and syntax
2. Include proper quoting and escaping
3. Add comments for complex operations
4. Ensure the command is safe and follows best practices
5. Handle multiple targets and options appropriately
6. Include error handling where necessary

Example Input:
Action: find
Target: /home/user
Option: -name
Parameter: pattern = "*.txt"

Example Output:
find /home/user -name "*.txt"

Your response should be ONLY the bash command, nothing else. Do not include any explanations or additional text.

Input: {structured_input}
Output:""" 