example_var = "グローバル変数"

class ExampleClass:
    # クラス変数
    example_var = "クラス変数"

    def call_method(self):
        def inner_function():
            example_var = "ローカル変数"
            return example_var

        return inner_function()

example_instance = ExampleClass()

print(example_instance.call_method())