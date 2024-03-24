import json
import ast


def convert_to_list_of_lists(ans):
    """
  Converts the output from the generative model to a list of lists.

  Args:
    ans: The output string from the generative model.

  Returns:
    A list of lists, where each inner list contains a question,
    the correct answer, and two incorrect answers.
  """

    # Remove potential whitespace and newline characters
    ans = ans.strip()

    # Check if the output starts and ends with square brackets
    if not (ans.startswith("[") and ans.endswith("]")):
        raise ValueError("Invalid output format: Output should be a list of lists.")

    # Use ast.literal_eval for safe evaluation of the string representation
    try:
        list_of_lists = ast.literal_eval(ans)
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Invalid output format: Unable to parse the string. Error: {e}")

    # Verify the format of each inner list
    for inner_list in list_of_lists:
        if not (isinstance(inner_list, list) and len(inner_list) == 4):
            raise ValueError("Invalid output format: Inner lists should contain 4 elements.")

    return list_of_lists


def lists_of_lists_to_json(data, filename):
    data = convert_to_list_of_lists(data)
    questions_data = []
    for question_info in data:
        question = question_info[0]
        answer = question_info[1]
        wrong_answer1 = question_info[2]
        wrong_answer2 = question_info[3]
        questions_data.append({
            "question": question,
            "answer": answer,
            "wrong_answer1": wrong_answer1,
            "wrong_answer2": wrong_answer2
        })

    with open(filename, "w") as json_file:
        json.dump(questions_data, json_file, indent=4)
