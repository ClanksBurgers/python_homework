# Assignment 2 Task 1 Diary

import traceback

try:
    with open("diary.txt", "a") as diary_file:
        first_prompt = True

        while True:
            try:
                if first_prompt:
                    line = input("What happened today? ")
                    first_prompt = False
                else:
                    line = input("what else? ")
            except EOFError:
                raise

            if line == "done for now":
                diary_file.write(line + "\n")
                break

            diary_file.write(line + "\n")

except Exception as e:
   trace_back = traceback.extract_tb(e.__traceback__)
   stack_trace = list()
   for trace in trace_back:
      stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
   print(f"Exception type: {type(e).__name__}")
   message = str(e)
   if message:
      print(f"Exception message: {message}")
   print(f"Stack trace: {stack_trace}")

