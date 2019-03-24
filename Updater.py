# -*- coding: utf-8 -*-

# The main class of this application
#
# Created by: WangKai,
#             College of Earth and Planetary Sciences (CEPS),
#             University of Chinese Academy of Sciences (UCAS).
#
# Updates: 2019/03/21 - V1.0, build and comment

import sys
import os
import re
import pickle
import json
from PyQt5 import QtWidgets, QtCore, QtGui
from requests_html import HTMLSession
from urllib import parse
from UpdaterGUI import Ui_Main
from LoginGUI import Ui_Login
from DialogGUI import Ui_Dialog

session = HTMLSession()
user_info = {'remember_user': True,
             'auto_login': True,
             'user_id': 'userId',
             'password': 'password',
             'org': 'organisation',
             'name': 'name',
             'file_path': '',
             'remember_select': True,
             'select_course': []}


class LoginMain(QtWidgets.QWidget, Ui_Login):
    def __init__(self):
        super(LoginMain, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.check_remember.setChecked(user_info['remember_user'])
        self.check_auto.setChecked(user_info['auto_login'])
        self.dialog = DialogMain()

    def auto_login(self):
        if user_info['remember_user'] and user_info['user_id'] != 'userId':
            self.edit_username.setText(user_info['user_id'])
            self.edit_password.setText(user_info['password'])
            if user_info['auto_login']:
                self.login()

    def button_login_click(self):
        if self.edit_username.text() and self.edit_password.text():
            user_info['user_id'] = self.edit_username.text()
            user_info['password'] = self.edit_password.text()
            self.login()
        else:
            self.dialog = DialogMain('警告', '用户名或密码不能为空！')
            self.dialog.show()

    def login(self):
        print("\n您的登录名为：%s" % user_info['user_id'])
        print("......................")
        print("登录中，稍安勿躁....")
        print("......................")
        self.button_login.setText('登录中...')
        try:
            session.get('http://onestop.ucas.ac.cn/home/index')  # 综合信息网
            post = {'username': user_info['user_id'], 'password': user_info['password'], 'remember': 'checked'}
            headers = {'Host': 'onestop.ucas.ac.cn',
                       'Referer': 'http://onestop.ucas.ac.cn/home/index',
                       'X-Requested-With': 'XMLHttpRequest',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
            r = session.post('http://onestop.ucas.ac.cn/Ajax/Login/0', data=post, headers=headers)
            if 'true' not in r.text:
                if 'false' in r.text:
                    self.dialog = DialogMain('错误', json.loads(r.text)['msg'])
                else:
                    self.dialog = DialogMain('错误', r.text)
                self.edit_password.setText('')
                self.dialog.show()
            else:
                url = json.loads(r.text)['msg']
                r = session.get(url)  # SEP 教育接入平台
                name_tag = r.html.find('li.btnav-info[title=当前用户所在单位]', first=True)
                if name_tag is None:
                    self.dialog = DialogMain('错误', '登录失败，请核对用户名和密码')
                    self.dialog.show()
                else:
                    name = name_tag.text
                    match = re.compile(r'\s*(\S*)\s*(\S*)\s*').match(name)
                    if match:
                        user_info['org'] = match.group(1)\
                            .replace('\xc2', '').replace('\x80', '').replace('\x90', '').strip()
                        user_info['name'] = match.group(2)\
                            .replace('\xc2', '').replace('\x80', '').replace('\x90', '').strip()
                        user_info['remember_user'] = self.check_remember.isChecked()
                        user_info['auto_login'] = self.check_auto.isChecked()
                        save_info()
                        self.updater = UpdaterMain()
                        self.updater.show()
                        self.updater.show_class()
                        self.close()
                    else:
                        self.dialog = DialogMain('错误', '登录失败，请核对用户名和密码')
                        self.dialog.show()
        except NameError as e:
            self.dialog = DialogMain('错误', str(e))
            self.dialog.show()


class DialogMain(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self, title='', message='', height=0):
        super(DialogMain, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        if title:
            self.setWindowTitle(title)
        if message:
            self.label_message.setText(message)
        if height:
            self.setFixedSize(self.width(), height)
            self.label_message.setGeometry(QtCore.QRect(20, 20, 360, height-60))
            self.button_ok.setGeometry(QtCore.QRect(330, height-30, 50, 20))
        else:
            self.setFixedSize(self.width(), self.height())


class UpdaterMain(QtWidgets.QWidget, Ui_Main):
    def __init__(self):
        super(UpdaterMain, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.update_file = {}
        self.class_list = []
        self.class_state = {}
        self.label_hello.setText('欢迎您！%s，%s' % (user_info['org'], user_info['name']))
        if not user_info['file_path']:
            user_info['file_path'] = os.getcwd()
        self.edit_path.setText(user_info['file_path'])
        self.check_remember.setChecked(user_info['remember_select'])
        self.model = QtGui.QStandardItemModel()
        self.list_course.setModel(self.model)
        self.list_course.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.button_update.setFocus()
        self.dialog = DialogMain()

    def show_class(self):
        r = session.get('http://sep.ucas.ac.cn/portal/site/16/801')  # 登录中间页
        new_url = r.html.find('noscript', first=True).find('meta', first=True).attrs.get('content')[6:]
        r = session.get(new_url)
        new_url = r.html.find('a#allSites', first=True).attrs.get('href')
        r = session.get(new_url)
        sakai_csrf_token = r.html.find('input[name=sakai_csrf_token]', first=True).attrs.get('value')
        post = {'eventSubmit_doChange_pagesize': 'changepagesize',
                'selectPageSize': 200,
                'sakai_csrf_token': sakai_csrf_token}
        new_url = re.sub('-reset', '', new_url)  # 去掉 -reset
        r = session.post(new_url, data=post)
        titles = r.html.find('td[headers=title]')
        self.class_list = []
        for title in titles[1:]:
            class_name = title.text.strip()  # 去掉字符串头尾的空格、换行符
            class_name = re.sub(r"[/\\:*\"<>|?]", "", class_name)
            class_id = title.find('a.getSiteDesc', first=True).attrs.get('id')
            class_website = title.find('a', first=True).attrs.get('href')
            self.class_list.append((class_id, class_name, class_website))
        sort_class = []
        first_group = '夏季'
        self.model.clear()
        self.class_state = {}
        for key in ['夏季', '春季', '秋季']:
            for class_info in self.class_list:
                if key in class_info[1]:
                    if not sort_class:
                        first_group = key
                    sort_class.append(class_info)
                    item_checked = QtGui.QStandardItem()
                    if not user_info['remember_select']:
                        item_checked.setCheckState([QtCore.Qt.Unchecked, QtCore.Qt.Checked][key == first_group])
                    elif class_info[1] in user_info['select_course']:
                        item_checked.setCheckState(QtCore.Qt.Checked)
                    else:
                        item_checked.setCheckState(QtCore.Qt.Unchecked)
                    item_checked.setCheckable(True)
                    item = QtGui.QStandardItem(class_info[1])
                    self.model.setItem(len(sort_class)-1, 0, item_checked)
                    self.model.setItem(len(sort_class)-1, 1, item)
                    self.model.setItem(len(sort_class)-1, 2, QtGui.QStandardItem(''))
                    self.list_course.resizeColumnsToContents()
                    self.class_state[class_info[1]] = [item_checked.checkState(), False]
        have_new_class_num = 0
        self.class_list = sort_class
        print("\n\n有更新的课件：")
        self.update_file = {}
        for row, c in enumerate(self.class_list):
            self.update_file[c[1]] = []
            url = c[2]
            r = session.get(url)  # 当前课程
            url = r.html.find('a.Mrphs-toolsNav__menuitem--link')[3].attrs.get('href')  # 左侧菜单栏 第4个”资源“
            print("\n===== %s =====" % c[1])
            flag = self.get_class(c[1], url, None, False)
            if flag:
                print('yes')
                self.model.item(row, 1).setForeground(QtGui.QBrush(QtGui.QColor(53, 116, 245)))
                self.class_state[c[1]][1] = True
                have_new_class_num += 1
        self.label_course.setText('<html><head/><body><p>已选 '
                                  + str(len(self.class_list)) +
                                  ' 门课程，<span style="color:#3574f5;">有 '
                                  + str(have_new_class_num) +
                                  ' 门更新：</span></p></body></html>')
        self.tree_update.clear()

    def get_class(self, current_class, url, data, download_or_not=True):
        have_new = False
        if data is not None:
            r = session.post(url, data=data)
        else:
            r = session.get(url)
        resource_list = r.html.find('tr')
        for res in resource_list[2:]:
            res_url = res.find('a', first=True).attrs.get('href')
            # 文件夹
            if res.find('a', first=True).attrs.get('title') == '打开此文件夹':
                path = res.find('a', first=True).attrs.get('onclick')
                reg = re.compile("Id'\).value='([\s\S]*)';document")
                match = reg.search(path)
                if match:
                    path = match.group(1)
                    reg = re.compile('name="sakai_csrf_token" value="(.*)"')
                    sakai_csrf_token = reg.search(r.text).group(1)
                    data = {'source': '0',
                            'collectionId': path,
                            'navRoot': '',
                            'criteria': 'title',
                            'sakai_action': 'doNavigate',
                            'rt_action': '',
                            'selectedItemId': '',
                            'itemHidden': 'false',
                            'itemCanRevise': 'false',
                            'sakai_csrf_token': sakai_csrf_token}
                    res_new = r.html.find('form', first=True).attrs.get('action')
                    dir_name = path.split('/')[-2]
                    dir_name = re.sub(r"[/\\:*\"<>|?]", "", dir_name)
                    dir_name = os.path.join(current_class, dir_name)
                    have_new = self.get_class(dir_name, res_new, data, download_or_not) or have_new
            # 有版权的文件，构造下载链接
            elif res.find('a', first=True).attrs.get('href') == '#':
                js_str = res.find('a', first=True).attrs.get('onclick')
                reg = re.compile(r"openCopyrightWindow\('(.*)','copyright")
                match = reg.match(js_str)
                if match:
                    res_url = match.group(1)
                    path = re.sub('http://course.ucas.ac.cn/access', '', res_url)
                    res_name = res.find("a")[1].text.replace("©", "").strip()
                    res_name = re.sub(r"[/\\:*\"<>|?]", "", res_name)
                    res_url = 'http://course.ucas.ac.cn/access/accept?ref=%s&url=%s' % (path, path)
                    have_new = self.download(res_url, res_name, current_class, download_or_not) or have_new
            # 课件可以直接下载的
            else:
                try:
                    res_name = parse.unquote(res_url.split('/')[-1])
                    res_name = re.sub(r"[/\\:*\"<>|?]", "", res_name)
                    have_new = self.download(res_url, res_name, current_class, download_or_not) or have_new
                except AttributeError as e:
                    print(e)
                    self.login = LoginMain()
                    self.login.show()
                    self.dialog = DialogMain('错误', '网络连接错误！')
                    self.dialog.show()
                    self.close()
        return have_new

    # 下载课件
    def download(self, url, file_name, class_name, download_or_not=True):
        # \xa0 转 gbk 会有错
        file_name = file_name.replace(u'\xa0', ' ').replace(u'\xc2', '')
        current_dir = os.path.join(user_info['file_path'], class_name)
        file = os.path.join(current_dir, file_name)
        # 存在该文件，返回
        if os.path.exists(file):
            return False
        else:
            c_path = os.path.join(class_name, file_name).split('/')
            c_name = c_path[0]
            c_dir = '/'.join(c_path[1:])
            self.update_file[c_name].append(c_dir)
        if download_or_not:
            print('正在下载 %s...' % file)
            # 没有课程文件夹则创建
            if not os.path.exists(current_dir):
                os.makedirs(current_dir)
            s = session.get(url)
            with open(file, 'wb') as data:
                data.write(s.content)
        else:
            print('有更新 %s...' % file)
            return True

    def button_about_click(self):
        self.dialog = DialogMain('关于', '国科大课件自动同步程序\n\n版本：V1.0\n更新日期：2019-03-22\n\n'
                                       '@233 工作室\n地球与行星科学学院\n中国科学院大学\n\n鸣谢：libowei1213@github', 240)
        self.dialog.show()

    def button_exit_click(self):
        msg = QtWidgets.QMessageBox.question(self, '提示', '确定要注销当前账号并重新登录吗？', QtWidgets.QMessageBox.Yes |
                                             QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if msg == QtWidgets.QMessageBox.Yes:
            self.login = LoginMain()
            self.login.show()
            self.close()

    def combo_term_changed(self):
        self.check_state()
        search_item = self.select_term.currentText()[:2]
        search_class = []
        if search_item == '全部':
            search_class = self.class_list
        else:
            for class_info in self.class_list:
                if search_item in class_info[1]:
                    search_class.append(class_info)
        self.show_search(search_class)

    def button_search_click(self):
        self.check_state()
        search_item = self.edit_search.text()
        search_class = []
        for class_info in self.class_list:
            if search_item in class_info[1]:
                search_class.append(class_info)
        self.show_search(search_class)

    def button_reset_click(self):
        self.check_state()
        self.edit_search.clear()
        self.show_search(self.class_list)

    def check_state(self):
        for index in range(self.model.rowCount()):
            self.class_state[self.model.data(self.model.index(index, 1))][0] = self.model.item(index, 0).checkState()

    def show_search(self, c_list):
        self.model.clear()
        for index, class_info in enumerate(c_list):
            item_checked = QtGui.QStandardItem()
            item_checked.setCheckState(self.class_state[class_info[1]][0])
            item_checked.setCheckable(True)
            item = QtGui.QStandardItem(class_info[1])
            self.model.setItem(index, 0, item_checked)
            self.model.setItem(index, 1, item)
            self.model.setItem(index, 2, QtGui.QStandardItem(''))
            self.list_course.resizeColumnsToContents()
            if self.class_state[class_info[1]][1]:
                self.model.item(index, 1).setForeground(QtGui.QBrush(QtGui.QColor(53, 116, 245)))

    def button_path_click(self):
        dir_choose = QtWidgets.QFileDialog.getExistingDirectory(self, '选择课件存放路径', os.getcwd())
        if dir_choose != '':
            self.edit_path.setText(dir_choose)
            user_info['file_path'] = dir_choose
            msg = QtWidgets.QMessageBox.question(self, '提示', '确定要更改课件存放路径吗？这可能需要一些时间来更新课件信息',
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                 QtWidgets.QMessageBox.Yes)
            if msg == QtWidgets.QMessageBox.Yes:
                self.show_class()
                self.dialog = DialogMain('提示', '课程信息已更新！')
                self.dialog.show()

    def button_update_click(self):
        select_list = []
        for index, class_info in enumerate(self.class_list):
            sate = self.model.item(index, 0).checkState()
            if sate == QtCore.Qt.Checked:
                select_list.append(class_info)
        self.button_update_main(select_list)

    def button_update_all_click(self):
        msg = QtWidgets.QMessageBox.question(self, '提示', '确定要下载所有更新的课件吗？', QtWidgets.QMessageBox.Yes |
                                             QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if msg == QtWidgets.QMessageBox.Yes:
            self.button_update_main(self.class_list)

    def button_update_main(self, c_list):
        for c in c_list:
            url = c[2]
            r = session.get(url)  # 当前课程
            url = r.html.find('a.Mrphs-toolsNav__menuitem--link')[3].attrs.get('href')  # 左侧菜单栏 第4个”资源“
            print("\n===== %s =====" % c[1])
            self.get_class(c[1], url, None)
        self.dialog = DialogMain('成功', '课件更新完毕！')
        self.dialog.show()

    def button_credit_click(self):
        self.dialog = DialogMain('提示', '功能仍在建设中...')
        self.dialog.show()

    def list_click(self):
        row = self.list_course.currentIndex().row()
        if row != -1:
            class_name = self.model.data(self.model.index(row, 1))
            self.tree_update.clear()
            root = QtWidgets.QTreeWidgetItem(self.tree_update)
            root.setText(0, class_name)
            class_files = self.update_file[class_name]
            last_tree = []
            for file in class_files:
                path = root
                file_tree = file.split('/')
                for index, file_dir in enumerate(file_tree):
                    if index < len(last_tree)-1 and file_dir == last_tree[index]:
                        path = path.child(path.childCount()-1)
                    else:
                        path = QtWidgets.QTreeWidgetItem(path)
                        path.setText(0, file_dir)
                last_tree = file_tree
            self.tree_update.expandAll()

    def select_all_changed(self):
        for index in range(self.model.rowCount()):
            self.model.item(index, 0).setCheckState(self.check_all.checkState())

    def closeEvent(self, a0: QtGui.QCloseEvent):
        user_info['remember_select'] = self.check_remember.isChecked()
        user_info['select_course'] = []
        self.check_state()
        for index, class_info in enumerate(self.class_list):
            sate = self.class_state[class_info[1]][0]
            if sate == QtCore.Qt.Checked:
                class_name = class_info[1]
                user_info['select_course'].append(class_name)
        save_info()


def read_info():
    global user_info
    if not os.path.exists(info_file):
        with open(info_file, 'wb') as file:
            pickle.dump(user_info, file, -1)
    else:
        with open(info_file, 'rb') as file:
            user_info = pickle.load(file)


def save_info():
    with open(info_file, 'wb') as file:
        pickle.dump(user_info, file, -1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    info_file = os.path.join(os.getcwd(), 'user.info')
    read_info()
    window_main = LoginMain()
    window_main.show()
    window_main.auto_login()
    sys.exit(app.exec_())
