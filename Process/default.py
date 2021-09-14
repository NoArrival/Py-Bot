#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Get_info_Message(object):
    """从元数据中提取关键信息"""

    def __init__(self,message):
        self.chat_id = message['message']['from']['id']
        self.type = self.reType(message)
        self.isUnknown = not(self.type == 'command' or self.type == 'text')      #检测是否为未知数据（即除command消息和普通文本消息外的消息）
        if self.isUnknown == 0:
            self.text = message['message']['text']
            self.command = self.reCommand(self.text)


    def reCommand(self,text):
        argv_list = text.split(' ')
        command = argv_list.pop(0)
        return command

    def reType(self, data):
        if 'document' in data['message'] :
            return 'document'
        elif 'photo' in data['message'] :
            return 'photo'
        elif 'entities' in data['message'] :
            return 'command'
        elif 'text' in data['message'] :
            return 'text'
        else:
            return 'unknown'