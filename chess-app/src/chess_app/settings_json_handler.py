from json import load

# lets get my dfs up and working.
# I have a few rules when doing my custom dfs
# upon dfs, we always add a title <h1>title</h1> where title is the parent to help users know what setting type they are editing
# - If a node is a mapping, we will go deeper
# - if a mapping has a bool, ie "some_key": True -> return:

BOOL_TEMPLATE = lambda value, title, id: f"""\
<div class="form-group">
  <label class="form-switch">
    <input type="checkbox" id="input-check-{id}" {"checked" if value else "unchecked"}>
    <i class="form-icon"></i>{title}
  </label>
</div>"""

NUMBER_TEMPLATE = lambda value, title, id: f"""\
<div class="form-group">
  <label class="form-label" for="input-example-1">{title}</label>
  <input class="form-input" type="number" id="input-number-{id}" placeholder="{value}">
</div>"""

TEXT_TEMPLATE = lambda value, title, id: f"""\
<div class="form-group">
  <label class="form-label" for="input-example-1">{title}</label>
  <input class="form-input" type="text" id="input-text-{id}" placeholder="{value}">
</div>"""


def list_2d_to_str(alist):
    astr = ""
    for y in alist:
        for x in y:
            astr += x + ""
        astr += "\n"
    return astr


def str_to_list_2d(astr):
    y_vals = []
    for line in astr.splitlines():
        x_vals = [x for x in line.split("") if x]  # Filter out empty strings
        y_vals.append(x_vals)
    return y_vals


#
#
# x1 = [
#     ["br", "bh", "bb", "bq", "bk", "bb", "bh", "br"],
#     ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
#     ["--", "--", "--", "--", "--", "--", "--", "--"],
#     ["--", "--", "--", "--", "--", "--", "--", "--"],
#     ["--", "--", "--", "--", "--", "--", "--", "--"],
#     ["--", "--", "--", "--", "--", "--", "--", "--"],
#     ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
#     ["wr", "wh", "wb", "wk", "wq", "wb", "wh", "wr"]]
#
# x2 = [
#     ["!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!"],
#     ["!!", "br", "bh", "bb", "bq", "bw", "bk", "bb", "bh", "br", "!!"],
#     ["!!", "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp", "!!"],
#     ["!!", "--", "--", "--", "--", "--", "--", "--", "--", "--", "!!"],
#     ["!!", "--", "--", "--", "--", "--", "--", "--", "--", "--", "!!"],
#     ["!!", "--", "--", "--", "--", "--", "--", "--", "--", "--", "!!"],
#     ["!!", "--", "--", "--", "--", "--", "--", "--", "--", "--", "!!"],
#     ["!!", "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp", "!!"],
#     ["!!", "wr", "wh", "wb", "wk", "ww", "wq", "wb", "wh", "wr", "!!"],
#     ["!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!!"]]
#
# x1_string = """bp, bp, bp, bp, bp, bp, bp, bp,
# --, --, --, --, --, --, --, --,
# --, --, --, --, --, --, --, --,
# --, --, --, --, --, --, --, --,
# --, --, --, --, --, --, --, --,
# wp, wp, wp, wp, wp, wp, wp, wp,
# wr, wh, wb, wk, wq, wb, wh, wr, """
#
# x2_string = """!!, !!, !!, !!, !!, !!, !!, !!, !!, !!, !!,
# !!, br, bh, bb, bq, bw, bk, bb, bh, br, !!,
# !!, bp, bp, bp, bp, bp, bp, bp, bp, bp, !!,
# !!, --, --, --, --, --, --, --, --, --, !!,
# !!, --, --, --, --, --, --, --, --, --, !!,
# !!, --, --, --, --, --, --, --, --, --, !!,
# !!, --, --, --, --, --, --, --, --, --, !!,
# !!, wp, wp, wp, wp, wp, wp, wp, wp, wp, !!,
# !!, wr, wh, wb, wk, ww, wq, wb, wh, wr, !!,
# !!, !!, !!, !!, !!, !!, !!, !!, !!, !!, !!, """

#
# print(list_2d_to_str(x1))
# print(list_2d_to_str(x2))
# print(str_to_list_2d(list_2d_to_str(x1)) == x1)
# print(str_to_list_2d(list_2d_to_str(x2)) == x2)


from json import dump, load


def write_json_to_file(data, file_path, **args):
    with open(file_path, 'w') as f:
        dump(data, f, **args)


def read_json_from_file(file_path, **args):
    with open(file_path, 'r') as f:
        return load(f, **args)


def dfs_get_json(data_obj, path: list):
    """
    :param data_obj:  a python dictionary
    :param path:      a path of nests to search until the last path is found
    :return:          the data in the last path
    """
    for key, item in data_obj.items():  # Fixed .items() method call
        if item == path[-1]:
            return item
        elif item == path[0]:
            return dfs_get_json(item, path[1:])
    raise TypeError("path specified not in json (python dict)", path)


def build_settings(datafile="config.json"):
    json_data = read_json_from_file(datafile)
    return dfs_build_html(json_data)
    # return (dfs_get_json(json_data, ["Game", "modes"]) == ["normal", "wizard"])


def dfs_build_html(data_obj, current_nest=1, init=True, title=None, is_textfield=False):
    result = ""

    if is_textfield:
        text = "\n".join(str(item) for item in data_obj) if isinstance(data_obj, list) else data_obj
        len_text = text.split("\n")
        print("text", len_text)
        return f"""<div class="form-group">
  <label class="form-label" for="input-field-{title}">{title}</label>
  <textarea class="form-input" id="input-field-{title}" placeholder="Textarea" rows="{len_text}">{data_obj}</textarea>
</div>"""

    if title:
        if isinstance(data_obj, str):
            val, title = data_obj, title
            my_id = title
            return TEXT_TEMPLATE(val, title, my_id)

        if isinstance(data_obj, bool):
            val, title = data_obj, title
            my_id = title
            return BOOL_TEMPLATE(val, title, my_id)

        if isinstance(data_obj, int):
            val, title = data_obj, title
            my_id = title
            return NUMBER_TEMPLATE(val, title, my_id)

        if isinstance(data_obj, float):
            val, title = data_obj, title
            my_id = title
            return NUMBER_TEMPLATE(val, title, my_id)

    # init only
    if init:
        result += "<div class=\"filter-nav\">"
        result += "<label class=\"chip\" for=\"tag-0\">All</label>"
        # set up the navigation menu
        i = 1
        for key, _ in data_obj.items():
            result += f"<label class=\"chip\" for=\"tag-{i}\">{key}</label>"
            i += 1

    if current_nest > 3:
        current_nest = 3
    i = 0
    for key, item in data_obj.items():
        print(key, item)
        if isinstance(item, dict):
            # its another nest, so add a header and move on

            # <div class="accordion">
            #   <input type="radio" id="accordion-1" name="accordion-radio" hidden>
            #   <label class="accordion-header" for="accordion-1">
            #     Title
            #   </label>
            #   <div class="accordion-body">
            #     <!-- Accordions content -->
            #   </div>
            # </div>
            result += f"""<div class="accordion">
              <input type="checkbox" id="accordion-{current_nest}-{key}" name="accordion-radio" hidden>
              <label class="accordion-header" for="accordion-{current_nest}-{key}">
                <i class="icon icon-arrow-right mr-1"></i>
                <h{current_nest}>{key}</h{current_nest}>
              </label>
              <div class="accordion-body">"""
            result += dfs_build_html(item, (current_nest + 1), init=False)
            result += """</div>
                        </div>"""
        elif isinstance(item, list):
            if True in [isinstance(item2, list) for item2 in item]:
                # double list (2d list)
                new_item_as_str = list_2d_to_str(item)
                result += dfs_build_html(item, current_nest + 1, False, title=key, is_textfield=True)

            else:
                result += dfs_build_html(list_2d_to_str(item), current_nest + 1, False, title=key, is_textfield=True)

        else:
            result += dfs_build_html(item, current_nest, False, key)
        # add the templates for each type, lists, nests
        i += 1
    return result


build_settings()

#
# def handle_value(value, path, key):
#     result = ''
#     if isinstance(value, bool):
#         result += handle_boolean(value, path, key)
#     elif isinstance(value, (int, float)):
#         result += handle_number(value, path, key)
#     elif isinstance(value, str):
#         result += handle_string(value, path, key)
#     elif isinstance(value, (list, tuple)):
#         if all(isinstance(item, str) for item in value):
#             result += handle_iterable_string(value, path, key)
#         elif all(isinstance(item, (list, tuple)) and all(isinstance(sub_item, str) for sub_item in item) for item in
#                  value):
#             result += handle_iterable_iterable_string(value, path, key)
#         elif all(isinstance(item, (int, float)) for item in value):
#             result += handle_iterable_number(value, path, key)
#         elif all(isinstance(item, bool) for item in value):
#             result += handle_iterable_boolean(value, path, key)
#         else:
#             # Generic iterable handling
#             pass
#     return result
