import json


def gen_pairs(wordMap):
    wordMap = sorted(wordMap.items(), key = lambda current:current[1], reverse=True)
    for first, second in wordMap:
        yield f"{first}: {second}"




if __name__ == '__main__':
    with open('./Logs/statistics.json', 'r') as file:
        data = json.load(file)

    with open('report.txt', 'w') as writer:
        writer.write(f'1. Number of Unique Pages: {data['uniquePages']} (successful queries: {data['successfulPages']}\n')
        writer.write(f'2. Longest Page: {data['longestPageUrl']} with word count {data['longestPageLength']}\n')
        writer.write(f'3. 50 most commonly seen words:\n\n')
        gen = gen_pairs(data['wordCounter'])
        for i in range(50):
            writer.write(f'{i + 1}. {next(gen)}\n')

        writer.write('\n4. Subdomains visited:\n\n')

        num = 1
        domains = sorted(data['domains'].items(), key = lambda current:current[0])
        for first, second in domains:
            writer.write(f'{num}. {first}, {second}\n')
            num += 1
     