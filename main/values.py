import math

class Value:
  def __init__(self):
    self.set_pos()
    self.set_context()

  def set_pos(self, pos_start=None, pos_end=None):
    self.pos_start = pos_start
    self.pos_end = pos_end
    return self

  def set_context(self, context=None):
    self.context = context
    return self

  def added_to(self, other):
    return None, self.illegal_operation(other)

  def subbed_by(self, other):
    return None, self.illegal_operation(other)

  def multed_by(self, other):
    return None, self.illegal_operation(other)

  def dived_by(self, other):
    return None, self.illegal_operation(other)

  def moded_by(self, other):
    return None, self.illegal_operation(other)

  def powed_by(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_eq(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_ne(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_lt(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_gt(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_lte(self, other):
    return None, self.illegal_operation(other)

  def get_comparison_gte(self, other):
    return None, self.illegal_operation(other)

  def anded_by(self, other):
    return None, self.illegal_operation(other)

  def ored_by(self, other):
    return None, self.illegal_operation(other)

  def notted(self, other):
    return None, self.illegal_operation(other)

  def execute(self, args):
    return RTResult().failure(self.illegal_operation())

  def copy(self):
    raise Exception('No copy method defined')

  def is_true(self):
    return False

  def illegal_operation(self, other=None):
    if not other: other = self
    return RTError(
      self.pos_start, other.pos_end,
      'Illegal operation',
      self.context
    )

class Number(Value):
  def __init__(self, value):
    super().__init__()
    self.value = value

  def to_realnum(self):
    num = float(self.value) if (float(self.value) % 1) else int(self.value)
    return num

  def added_to(self, other):
    if isinstance(other, Number):
      return Number(self.value + other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def subbed_by(self, other):
    if isinstance(other, Number):
      return Number(self.value - other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def multed_by(self, other):
    if isinstance(other, Number):
      return Number(self.value * other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def dived_by(self, other):
    if isinstance(other, Number):
      if other.value == 0:
        return None, RTError(
          other.pos_start, other.pos_end,
          'Division by zero',
          self.context
        )

      return Number(self.value / other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def moded_by(self, other):
    if isinstance(other, Number):
      if other.value == 0:
        return None, RTError(
          other.pos_start, other.pos_end,
          'Mod by zero',
          self.context
        )

      return Number(self.value % other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def powed_by(self, other):
    if isinstance(other, Number):
      return Number(self.value ** other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_eq(self, other):
    if isinstance(other, Number):
      return Number(int(self.value == other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_ne(self, other):
    if isinstance(other, Number):
      return Number(int(self.value != other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_lt(self, other):
    if isinstance(other, Number):
      return Number(int(self.value < other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_gt(self, other):
    if isinstance(other, Number):
      return Number(int(self.value > other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_lte(self, other):
    if isinstance(other, Number):
      return Number(int(self.value <= other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def get_comparison_gte(self, other):
    if isinstance(other, Number):
      return Number(int(self.value >= other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def anded_by(self, other):
    if isinstance(other, Number):
      return Number(int(self.value and other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def ored_by(self, other):
    if isinstance(other, Number):
      return Number(int(self.value or other.value)).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def notted(self):
    return Number(1 if self.value == 0 else 0).set_context(self.context), None

  def copy(self):
    copy = Number(self.value)
    copy.set_pos(self.pos_start, self.pos_end)
    copy.set_context(self.context)
    return copy

  def is_true(self):
    return self.value != 0

  def __str__(self):
    return str(self.value)
  
  def __repr__(self):
    return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)
Number.math_E = Number(math.e)

class String(Value):
  def __init__(self, value):
    super().__init__()
    self.value = value

  def added_to(self, other):
    if isinstance(other, String):
      return String(self.value + other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def multed_by(self, other):
    if isinstance(other, Number):
      return String(self.value * other.value).set_context(self.context), None
    else:
      return None, Value.illegal_operation(self, other)

  def is_true(self):
    return len(self.value) > 0

  def copy(self):
    copy = String(self.value)
    copy.set_pos(self.pos_start, self.pos_end)
    copy.set_context(self.context)
    return copy

  def __str__(self):
    return self.value

  def __repr__(self):
    return f'"{self.value}"'

class BaseFunction(Value):
  def __init__(self, name):
    super().__init__()
    self.name = name or "<anonymous>"

  def generate_new_context(self):
    new_context = Context(self.name, self.context, self.pos_start)
    new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
    return new_context

  def check_args(self, arg_names, args):
    res = RTResult()

    if len(args) > len(arg_names):
      return res.failure(RTError(
        self.pos_start, self.pos_end,
        f"{len(args) - len(arg_names)} too many args passed into {self}",
        self.context
      ))
    
    if len(args) < len(arg_names):
      return res.failure(RTError(
        self.pos_start, self.pos_end,
        f"{len(arg_names) - len(args)} too few args passed into {self}",
        self.context
      ))

    return res.success(None)

  def populate_args(self, arg_names, args, exec_ctx):
    for i in range(len(args)):
      arg_name = arg_names[i]
      arg_value = args[i]
      arg_value.set_context(exec_ctx)
      exec_ctx.symbol_table.set(arg_name, arg_value)

  def check_and_populate_args(self, arg_names, args, exec_ctx):
    res = RTResult()
    res.register(self.check_args(arg_names, args))
    if res.should_return(): return res
    self.populate_args(arg_names, args, exec_ctx)
    return res.success(None)

class Function(BaseFunction):
  def __init__(self, name, body_node, arg_names, should_auto_return):
    super().__init__(name)
    self.body_node = body_node
    self.arg_names = arg_names
    self.should_auto_return = should_auto_return

  def execute(self, args):
    res = RTResult()
    interpreter = Interpreter()
    exec_ctx = self.generate_new_context()

    res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
    if res.should_return(): return res

    value = res.register(interpreter.visit(self.body_node, exec_ctx))
    if res.should_return() and res.func_return_value == None: return res

    ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
    return res.success(ret_value)

  def copy(self):
    copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
    copy.set_context(self.context)
    copy.set_pos(self.pos_start, self.pos_end)
    return copy

  def __repr__(self):
    return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
  def __init__(self, name):
    super().__init__(name)

  def execute(self, args):
    res = RTResult()
    exec_ctx = self.generate_new_context()

    method_name = f'execute_{self.name}'
    method = getattr(self, method_name, self.no_visit_method)

    res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
    if res.should_return(): return res

    return_value = res.register(method(exec_ctx))
    if res.should_return(): return res
    return res.success(return_value)
  
  def no_visit_method(self, node, context):
    raise Exception(f'No execute_{self.name} method defined')

  def copy(self):
    copy = BuiltInFunction(self.name)
    copy.set_context(self.context)
    copy.set_pos(self.pos_start, self.pos_end)
    return copy

  def __repr__(self):
    return f"<built-in function {self.name}>"

  #####################################

  def execute_print(self, exec_ctx):
    print(str(exec_ctx.symbol_table.get('value')))
    return RTResult().success(Number.null)
  execute_print.arg_names = ['value']
  
  def execute_print_ret(self, exec_ctx):
    return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
  execute_print_ret.arg_names = ['value']
  
  def execute_input(self, exec_ctx):
    if exec_ctx.symbol_table.get('help'):
      text = input(String(str(exec_ctx.symbol_table.get('help')) + " "))
    else:
      text = input()
    return RTResult().success(String(text))
  execute_input.arg_names = ['help']

  def execute_input_int(self, exec_ctx):
    while True:
      text = input()
      try:
        number = int(text)
        break
      except ValueError:
        print(f"'{text}' must be an integer. Try again!")
    return RTResult().success(Number(number))
  execute_input_int.arg_names = []

  def execute_clear(self, exec_ctx):
    os.system('cls' if os.name == 'nt' else 'cls') 
    return RTResult().success(Number.null)
  execute_clear.arg_names = []

  def execute_is_number(self, exec_ctx):
    is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
    return RTResult().success(Number.true if is_number else Number.false)
  execute_is_number.arg_names = ["value"]

  def execute_is_string(self, exec_ctx):
    is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
    return RTResult().success(Number.true if is_number else Number.false)
  execute_is_string.arg_names = ["value"]

  def execute_is_function(self, exec_ctx):
    is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
    return RTResult().success(Number.true if is_number else Number.false)
  execute_is_function.arg_names = ["value"]

  def execute_flr(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "FLR : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(math.floor(num.to_realnum())))
  execute_flr.arg_names = ["value"]

  def execute_cil(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "CIL : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(math.ceil(num.to_realnum())))
  execute_cil.arg_names = ["value"]

  def execute_log(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "LOG : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.log10(num.to_realnum()),2)))
  execute_log.arg_names = ["value"]

  def execute_sqrt(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "SQRT : Argument must be an Integer",
        exec_ctx
      ))

    square = math.sqrt(num.to_realnum())

    if square % 1:
      return RTResult().success(String('SQRT(%s)' % round(square,2)))
    else:
      return RTResult().success(Number(int(square)))
  execute_sqrt.arg_names = ["value"]

  def execute_sin(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "SIN : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.sin(num.to_realnum()),2)))
  execute_sin.arg_names = ["value"]

  def execute_cos(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "COS : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.cos(num.to_realnum()),2)))
  execute_cos.arg_names = ["value"]

  def execute_cot(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "COT : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round((1/math.tan(num.to_realnum())),2)))
  execute_cot.arg_names = ["value"]

  def execute_tan(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "TAN : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.tan(num.to_realnum()),2)))
  execute_tan.arg_names = ["value"]

  def execute_asin(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "ASIN : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.asin(num.to_realnum()),2)))
  execute_asin.arg_names = ["value"]

  def execute_acos(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "ACOS : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.acos(num.to_realnum()),2)))
  execute_acos.arg_names = ["value"]

  def execute_acot(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "ACOT : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round((math.pi/2) - math.atan(num.to_realnum()),2)))
  execute_acot.arg_names = ["value"]

  def execute_atan(self, exec_ctx):
    num = exec_ctx.symbol_table.get("value")

    if not isinstance(num, Number):
      return RTResult().failure(RTError(
        self.pos_start,self.pos_end,
        "ATAN : Argument must be an Integer",
        exec_ctx
      ))

    return RTResult().success(Number(round(math.atan(num.to_realnum()),2)))
  execute_atan.arg_names = ["value"]

  def execute_run(self, exec_ctx):
    fn = exec_ctx.symbol_table.get("fn")

    if not isinstance(fn, String):
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        "Second argument must be string",
        exec_ctx
      ))

    fn = fn.value

    try:
      with open(fn, "r") as f:
        script = f.read()
    except Exception as e:
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        f"Failed to load script \"{fn}\"\n" + str(e),
        exec_ctx
      ))

    _, error = run(fn, script)
    
    if error:
      return RTResult().failure(RTError(
        self.pos_start, self.pos_end,
        f"Failed to finish executing script \"{fn}\"\n" +
        error.as_string(),
        exec_ctx
      ))

    return RTResult().success(Number.null)
  execute_run.arg_names = ["fn"]
