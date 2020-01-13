# 与最新版整合

fork一个项目后，我们的项目副本也就保持在当时版本，当原项目更新后，我们的项目副本并不会更新。  

本文档介绍下如何将我们的项目副本更新到最新，即使我们已在项目副本上进行过改动。  

我们以[本项目](https://github.com/fakedon/checkin)为例,项目地址：[https://github.com/fakedon/checkin](https://github.com/fakedon/checkin)  

我们fork后地址：https://github.com/用户名/checkin

首先，访问我们的fork地址，并点击如图所示的compare
![](/docs/img/fork/click_compare.jpg)  

然后，需要特别注意，前面为项目副本，后面为原项目，如图所示
![](/docs/img/fork/compare_page.jpg)  
此时地址类似 
https://github.com/用户名/checkin/compare/master...fakedon:master  
当然你也可以替换用户名后直接访问上面网址，如果如上所示则不用修改，之后点击左下Create pull request，会出现如下图表格，按图示填写再次点击右下Create pull request  
![](/docs/img/fork/create_pull_request.jpg)  

之后页面会转到如下图，点击左下Rebase and merge，整个操作也就完成，我们的项目副本就会把原项目的更新同步到我们的项目副本，如果没冲突也会保持我们自己进行的改动。
![](/docs/img/fork/rebase_and_merge.jpg)  
