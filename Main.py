import codecs
doctype = '<!DOCTYPE html\n'


def meta_wrap(el_type, **kwargs):
    kwline = ""
    for k, v in kwargs.items():
        kwline += ' '+str(k) + '=' + '"' + str(v) + '"'
    kwline += ' '
    if len(el_type) == 0:
        return ""
    return "<"+el_type+kwline+">\n"


def html_wrap(text, el_type="div", el_class="", cr=True, **kwargs):
    kwline = ""
    for k, v in kwargs.items():
        kwline += ' '+str(k) + '=' + '"' + str(v) + '"'
    kwline += ' '
    if len(el_type) == 0:
        return text
    if len(el_class) > 0:
        cl_field = r" class={1} "
    else:
        cl_field = ""

    if cr:
        car_return = "\n"
    else:
        car_return = ""

    if len(text) == 0:
        return ("<{0}"+cl_field+kwline+"/>").format(el_type, el_class)
    else:
        return ("<{0}"+cl_field+kwline+">"+car_return+text+car_return+"</{0}>").format(el_type, el_class)


def p_wrap(text, el_class=""):
    return html_wrap(text, el_type="p", el_class=el_class, cr=False)


def li_wrap(text):
    return html_wrap(text, el_type="li", el_class="", cr=False)


# def list_wrap(texts=[""], el_class=""):
#     string = "\n"
#     for item in texts:
#         string += (li_wrap(item)+"\n")
#     return html_wrap(string, el_type="ol", el_class=el_class, cr=False)


def quest_wrap(text, number, aux_title=""):
    if len(aux_title) > 0:
        title = ' ' + aux_title
    else:
        title = ''
    h = html_wrap('Вопрос ' + str(number) + title, el_class='question_marker')
    return html_wrap(text=h+text, el_class="question")


def dump_html():
    with codecs.open("output.html", 'w', encoding='utf-8') as fh:
        fh.write(doctype)  # it produces a strange bug
        head = meta_wrap('link', rel="stylesheet", type="text/css", href="stylesheet.css")
        head += meta_wrap('meta', charset='utf-8')
        head += html_wrap('Title', 'title')
        head = html_wrap(head, 'head')
        body = html_wrap('Tour', el_class='tour') + html_wrap('bold text', el_class='question')
        body += quest_wrap('quest text', 13)
        body += stack_to_html(parse_4s_to_stack())
        body = html_wrap(body, 'body')

        fh.write(html_wrap(head+body, 'html', el_class="",  lang='ru'))

tokens = {
    "###LJ": {},  # will ignore it
    "###": {},  # заголовок
    "#EDITOR": {},  # редактор
    "#DATE": {},
    "#": {},  # generic comment
    "?": {'html_text': "Вопрос ", 'html_class': "question"},  # question text
    "!": {'html_text': "Ответ(ы): ", 'html_class': "answer"},  # answer
    "^": {'html_text': "Источник(и): ", 'html_class': "source"},  # source
    "№№": {},  # set question number and continue with that numbering
    "№": {},  # set one question number
    "=": {'html_text': "Зачёт: ", 'html_class': "answer"},  # other correct answers
    "/": {'html_text': "Комментарии: ", 'html_class': "comments"},  # comments to answer
    "@": {'html_text': "Автор(ы): ", 'html_class': "author"},  # authors
    "-": {},  # list
}


def starts_with_token(line):
    for token in tokens:
        if line.startswith(token):
            return True, token, line[len(token):]
    return False, "", line


def parse_4s_to_stack():
    stack = list()
    cur_text = ''
    cur_token = ''
    with codecs.open('quest.4s', 'r', 'utf8') as fh:
        for l in fh.readlines():
            res, token, line = starts_with_token(line=l.rstrip())
            if not res:
                cur_text += ("<br/>"+line)
                # cur_text += (html_wrap(line, el_type='p', el_class='what'))
            else:
                if token != cur_token:
                    stack.append((cur_token, cur_text))
                    cur_token = token
                    cur_text = line
                elif token == '-' and cur_token == '-':
                    stack.append((cur_token, cur_text.lstrip()))
                    cur_text = line
                else:
                    print('Specifications violation at line ' + l)
    stack.append((cur_token, cur_text))
    stack.reverse()
    stack.pop()
    print(stack)
    return stack
    # print(stack.pop())


def stack_to_html(stack):
    out = ""
    if len(stack) > 0:
        token, text = stack.pop()
        info = tokens.get(token, {})
        if token in ['@', '!', '^', '/', '=']:
            t = html_wrap(info.get('html_text', ""), el_class="field_header", cr=False)
            treat = flush_list(stack)
            out += html_wrap(text=t + text + treat, el_class=info.get('html_class', ""))
            return out + "\n" + stack_to_html(stack=stack)
        elif token == '?':
            return html_wrap(html_wrap(info.get("html_text", ""), el_class="question_header")
                             + text
                             + flush_list(stack)
                             + stack_to_html(stack),
                             el_class=info.get("html_class"),)
        else:
            return "still can't process " + token + ' ' + text + stack_to_html(stack)
            # elif token == '!':

    else:
        return out


def flush_list(stack):
    treat = ""
    if (len(stack) > 0) and (stack[-1][0] == '-'):
        while (len(stack) > 0) and (stack[-1][0] == '-'):
            treat += '\n' + li_wrap(stack.pop()[1])
        treat = html_wrap(text=treat, el_type='ol', cr=False)
    return treat


# def answer
# print(list_wrap(["lorem", "ipsum"]))
# print(list_wrap([]))
dump_html()
parse_4s_to_stack()

stakk = [ ('-', 'first one'), ('-','second one '), ('@', ''), ('!', 'ура!')]
# print(stack_to_html(stack=stakk))

print(stack_to_html(parse_4s_to_stack()))
