from subprocess import *
import json

# judge文件的路径
judge_path = 'python ./judge.py'

bot_path = ['', '', '']
for j in range(3):
    # bot文件的路径
    bot_path[j] = 'python ./bot/bot{}.py'.format(j+1)

# judge初始化
# (如果进行自博弈，需要进行随机初始化，这里是固定的)
with open('./init.json', 'r') as f:
    judge_input_json = json.load(f)


# 给bot发送命令，返回bot的输出
def send_input_to_bot(input_json, bot_id):
    input_str = json.dumps(input_json)
    bot_proc = Popen(bot_path[bot_id], stdin=PIPE, stdout=PIPE, shell=True)
    bot_proc.stdin.write(input_str.encode('UTF-8'))
    bot_proc.stdin.close()
    ret_bytes = bot_proc.stdout.readlines()
    bot_proc.terminate()
    ret_str = ''
    for tstr in ret_bytes:
        real_str = tstr.decode()
        real_str = real_str.replace('\t', '')
        ret_str += real_str.replace('\n', '')
    bot_output_json = json.loads(ret_str)
    return bot_output_json


# 给judge发送命令，返回judge的输出
def send_input_to_judge(input_json):
    input_str = json.dumps(input_json)
    judge_proc = Popen(judge_path, stdin=PIPE, stdout=PIPE)
    judge_proc.stdin.write(input_str.encode('UTF-8'))
    judge_proc.stdin.close()
    ret_bytes = judge_proc.stdout.readlines()
    judge_proc.terminate()
    ret_str = ''
    for tstr in ret_bytes:
        real_str = tstr.decode()
        real_str = real_str.replace('\t', '')
        ret_str += real_str.replace('\n', '')
    judge_output_json = json.loads(ret_str)
    return judge_output_json


# 交互示例
player_input = [{}, {}, {}]
for p in range(3):
    player_input[p]['requests'] = []
    player_input[p]['responses'] = []
step = 0
while True:
    step += 1
    print('step: ', step)
    judge_output_json = send_input_to_judge(judge_input_json)
    command = judge_output_json['command']
    if command == 'finish':
        print('finish')
        break
    judge_input_json['log'].append({'output': judge_output_json})
    po = judge_output_json['content']
    for key in po:
        tplayer = int(key)
        player_input[tplayer]['requests'].append(po[key])
        print('po[key]', po[key])
    judge_input_json['log'].append({})

    bot_output_json = send_input_to_bot(player_input[(step-1)%3], (step-1)%3)
    player_input[(step-1)%3]['responses'].append(bot_output_json['response'])
    judge_input_json['log'][-1][str((step-1)%3)] = {'response': bot_output_json['response'], 'verdict': 'OK'}

    print(judge_input_json['log'][-1])