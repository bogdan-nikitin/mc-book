INPUT = '''Now principles discovered off increasing how reasonably middletons men. Add seems out man met plate court sense. His joy she worth truth given. All year feet led view went sake. You agreeable breakfast his set perceived immediate. Stimulated man are projecting favourable middletons can cultivated. Tolerably earnestly middleton extremely distrusts she boy now not. Add and offered prepare how cordial two promise. Greatly who affixed suppose but enquire compact prepare all put. Added forth chief trees but rooms think may. Wicket do manner others seemed enable rather in. Excellent own discovery unfeeling sweetness questions the gentleman. Chapter shyness matters mr parlors if mention thought. Kindness to he horrible reserved ye. Effect twenty indeed beyond for not had county. The use him without greatly can private. Increasing it unpleasant no of contrasted no continuing. Nothing colonel my no removed in weather. It dissimilar in up devonshire inhabiting. He difficult contented we determine ourselves me am earnestly. Hour no find it park. Eat welcomed any husbands moderate. Led was misery played waited almost cousin living. Of intention contained is by middleton am. Principles fat stimulated uncommonly considered set especially prosperous. Sons at park mr meet as fact like. Too cultivated use solicitude frequently. Dashwood likewise up consider continue entrance ladyship oh. Wrong guest given purse power is no. Friendship to connection an am considered difficulty. Country met pursuit lasting moments why calling certain the. Middletons boisterous our way understood law. Among state cease how and sight since shall. Material did pleasure breeding our humanity she contempt had. So ye really mutual no cousin piqued summer result. However venture pursuit he am mr cordial. Forming musical am hearing studied be luckily. Ourselves for determine attending how led gentleman sincerity. Valley afford uneasy joy she thrown though bed set. In me forming general prudent on country carried. Behaved an or suppose justice. Seemed whence how son rather easily and change missed. Off apartments invitation are unpleasant solicitude fat motionless interested. Hardly suffer wisdom wishes valley as an. As friendship advantages resolution it alteration stimulated he or increasing. Inhabiting discretion the her dispatched decisively boisterous joy. So form were wish open is able of mile of. Waiting express if prevent it we an musical. Especially reasonable travelling she son. Resources resembled forfeited no to zealously. Has procured daughter how friendly followed repeated who surprise. Great asked oh under on voice downs. Law together prospect kindness securing six. Learning why get hastened smallest cheerful. Death there mirth way the noisy merit. Piqued shy spring nor six though mutual living ask extent. Replying of dashwood advanced ladyship smallest disposal or. Attempt offices own improve now see. Called person are around county talked her esteem. Those fully these way nay thing seems. Any delicate you how kindness horrible outlived servants. You high bed wish help call draw side. Girl quit if case mr sing as no have. At none neat am do over will. Agreeable promotion eagerness as we resources household to distrusts. Polite do object at passed it is. Small for ask shade water manor think men begin. Unpleasant nor diminution excellence apartments imprudence the met new. Draw part them he an to he roof only. Music leave say doors him. Tore bred form if sigh case as do. Staying he no looking if do opinion. Sentiments way understood end partiality and his. '''SYMBOLS_SIZE = {    # Uppercase    'A': 5,    'B': 5,    'C': 5,    'D': 5,    'E': 5,    'F': 5,    'G': 5,    'H': 5,    'I': 3,    'J': 5,    'K': 5,    'L': 5,    'M': 5,    'N': 5,    'O': 5,    'P': 5,    'Q': 5,    'R': 5,    'S': 5,    'T': 5,    'U': 5,    'V': 5,    'W': 5,    'X': 5,    'Y': 5,    'Z': 5,    # Lowercase    'a': 5,    'b': 5,    'c': 5,    'd': 5,    'e': 5,    'f': 4,    'g': 5,    'h': 5,    'i': 1,    'j': 5,    'k': 4,    'l': 2,    'm': 5,    'n': 5,    'o': 5,    'p': 5,    'r': 5,    's': 5,    't': 3,    'u': 5,    'v': 5,    'w': 5,    'x': 5,    'y': 5,    'z': 5,    # Symbols    ' ': 5,  # min space size is 1    '.': 1,}MAX_LINE_LEN = 113  # value in pixelsMAX_LINES = 14# MAX_PAGE_LEN = MAX_LINE_LEN * MAX_LINESdef get_word_len(word):    if not word:        return 0    # 'len(word) - 1' is for gaps between symbols    return sum(SYMBOLS_SIZE.get(c, 5) for c in word) + len(word) - 1def split_words_and_newlines(text):    parts = []    last_word = ''    newline = False    for char in text:        if char == ' ':            parts += [last_word]            last_word = ''            newline = False        elif char == '\n':            if not newline:                parts += [last_word]                last_word = ''            parts += ['\n']            newline = True        else:            last_word += char            newline = False    if not newline:        parts += [last_word]    return partsdef join_parts(parts):    if not parts:        return ''    joined = parts[0]    is_last_newline = False    for part in parts[1:]:        if part != '\n':            if is_last_newline:                joined += ' '            is_last_newline = True        else:            is_last_newline = False        joined += part    return joined# class Part: type: GAP | NEWLINE | WORD, value: str# def is_overflow(line_len, is_last_gap)# TODO: Newlinesdef split_on_pages(text):    pages = [[]]    # page_len = 0    line_len = 0    lines_count = 1    i = 0    words = split_words_and_newlines(text)    # words = text.replace('\n', ' \n ').split(' ')    for word in words:        if word == '\n':            pages[-1] += ['\n']            lines_count += 1            if lines_count > MAX_LINES:                pages += [[]]                lines_count = 1            line_len = 0        else:            word_len = get_word_len(word)            if word_len >= MAX_LINE_LEN:                for i in range(word_len // MAX_LINE_LEN):                    pages[-1] += word[i * MAX_LINE_LEN:(i + 1) * MAX_LINE_LEN]                    lines_count += 1                    if lines_count > MAX_LINES:                        pages += [[]]                        lines_count = 1                pages[-1] += [                    word[(i + 1) * MAX_LINE_LEN:(i + 2) * MAX_LINE_LEN]                ]                line_len = word_len % MAX_LINE_LEN            else:                if line_len + SYMBOLS_SIZE[' '] + word_len > MAX_LINE_LEN:                    line_len = word_len                    lines_count += 1                    if lines_count > MAX_LINES:                        pages += [[]]                        lines_count = 1                else:                    if line_len > 0:  # TODO: blank symbols                        line_len += SYMBOLS_SIZE[' ']                    line_len += word_len            pages[-1] += [word]    for page in pages:        print(join_parts(page))        print('=' * 20)def main():    split_on_pages('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii  abc')    # split_on_pages(INPUT)if __name__ == '__main__':    main()