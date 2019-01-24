# !!!!!! 
～～ csdn界面修改，此代码已经无法使用，具体是在用户所有文章的列表页无法拿到此用户的文章的总页数，有时间会进行修改。～～
感谢网友@Gerrard-YNWA  ，代码已修改至可以使用！

# csdn_to_hexo_markdown

# 前言
&emsp;使用了开源项目[html2text](https://github.com/aaronsw/html2text)
<br/>&emsp;修改自[网络代码](https://github.com/gaocegege/csdn-blog-export)，但是原代码在解析html时出错，应该是csdn的前端中间改了。
<br/>&emsp;网络代码可以转换成html和markdown，但是我修改成只能转markdown而且还进行了很多优化。增加了分类、标签等。
  
# 介绍
&emsp;代码把csdn的博客转成hexo接受的形式markdown。代码很全面，把hexo写文章时需要的头（title、tags、categories、copyright）都生成了。
<br/>&emsp;转化后的文章保存在markdown文件夹下。
<br/>&emsp;使用文章名字作为文件名字（可能会出问题，看下面“问题”部分的详解）。
# 使用
&emsp;有四个可选参数，csdn用户名name、转化类型type(默认是markdown，也只能是markdown)、
<br/>&emsp;转化的第几页page、
<br/>&emsp;只转化某篇文章
## 方法1：
&emsp;转化用户name的所有文章
```
 python toHexo.py --name u123456 --type markdown
```
## 方法2：
&emsp;转化用户第page页的文章
```
  python toHexo.py --name u123456 --type markdown --page 1
```
## 方法3：
&emsp;只转化某篇文章url
```
  python toHexo.py --url https://blog.csdn.net/u123456/article/details/51429540
```
# 问题
&emsp;1.名字中可能包含特殊字符出错，特别是在windows下。101行的代码已经对/进行了处理。
<br/>&emsp;如果问题很多懒得解决，把154行的注释放开做稍微修改，用文章url里的数字作为文章名字。
<br/>&emsp;2.文章使用网络上的代码，因此可能会有多余的代码，没有删除可能。
