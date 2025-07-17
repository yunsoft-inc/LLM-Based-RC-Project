![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=10&height=200&text=LLM%20BASED%20SELF%20DRIVING%20CAR&fontSize=40&animation=twinkling&fontAlign=40&fontAlignY=36)
# LLM 기반 자율 주행 자동차
## Hanyoung HighSchool 2025 Project

![Build Status](https://img.shields.io/badge/python-3776AB?style=flat-square&logo=html5&logoColor=000000)
![img1](https://github.com/yunsoft-inc/LLM-Based-RC-Project/blob/main/rc.png)

## 개발 동기
ChatGPT의 기술이 빠르게 발전하면서 다양한 기능들(이미지 설명, 실시간 대화 등)이 가능해졌음.
이러한 발전을 보다 보니 문득, RC카에 ChatGPT를 연동시키면 사람이 운전하듯이 자동차를 조종하는 자율 주행 자동차를 만들 수 있겠다는 생각이 들었고, 이 아이디어를 실행으로 옮기게 되었음.

## 제작에 들어간 기술들
- Python
메인 코드 작성 언어
- ChatGPT API
LLM으로 이미지 분석을 하기 위한 서비스
- ElevenLabs TTS API
음성 합성 기술
- 3D 프린팅
특수 RC카 바디 제작
- Arduino C
모터 제어, 명령 처리
- Html, JS
원격 조작 프로그램 개발
- Firebase Realtime Database, Storage, Hosting
원격 제어 서버 구축

## 프로그램에 사용된 기능들
- TTS(Text-To-Speech)
- LM(Large-Language-Model)
- 사진 촬영 및 심도 측정
- 모터 방향 및 속도 제어
- LLM 프롬프트 설계

## 작품을 개발하면서 어려웠던 점
ChatGPT에게 이미지를 인식하고 설명하도록 명령을 했더니, 사람이 감지되거나 사진에 아무 특징이 없으면 모든 형식을 무시하고 명령을 거부하는 문제가 존재했다. 이러한 문제를 해결하기 위해 검열을 피하게끔 최대한 단순하게 이미지를 설명하도록 프롬프트를 수정하고, 명령을 거부해도 출력 형식을 유지하기 위해 프롬프트를 수정했다.

고용량 배터리, 라즈베리파이, 아두이노, 스피커, 카메라를 모두 얹어서 RC카에 장착하니 무게로 인해 부하가 크게 걸려 제대로 움직이지 못하거나, 조금의 턱이 있으면 넘지를 못해 끼어버리는 문제가 있었다. 이러한 문제를 해결하기 위해 모터와 바퀴의 위치를 앞쪽으로 바꾸고, 후방에 볼캐스터를 추가 장착하여 안정성을 향상시켰다. 또한 무게중심도 안정적으로 조절하여 이동하고 정지할 때 관성으로 기우뚱거리는 문제도 해결했다.


## 작품을 만들면서 보람을 느낀점은 무엇인가?
설계한 RC카가 계획 했던대로 잘 작동하니 보람을 느꼈다.
주변 동아리 친구들에게 작품에 대한 피드백을 받으면서 내가 보완해야 할 점을 알게 되었기도 했지만, 작품을 잘 만들었다는 칭찬을 받을 때 보람을 느꼈다.

## 프로그램 개발 후 향후 진로에 미치는 영향
ChatGPT와 같은 LLM과, ElevenLabs와 같은 음성 합성 AI 모델의 무궁무진한 활용 가능성을 보았고, 컴퓨터, 전기전자, 인공지능 관련 분야로 대학 진학을 해, 관련 기술을 더 깊이 있게 배워, 더 큰 프로젝트를 진행해보고 싶다는 생각이 들었다.
> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Tech

Dillinger uses a number of open source projects to work properly:

- [AngularJS] - HTML enhanced for web apps!
- [Ace Editor] - awesome web-based text editor
- [markdown-it] - Markdown parser done right. Fast and easy to extend.
- [Twitter Bootstrap] - great UI boilerplate for modern web apps
- [node.js] - evented I/O for the backend
- [Express] - fast node.js network app framework [@tjholowaychuk]
- [Gulp] - the streaming build system
- [Breakdance](https://breakdance.github.io/breakdance/) - HTML
to Markdown converter
- [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

## Installation

Dillinger requires [Node.js](https://nodejs.org/) v10+ to run.

Install the dependencies and devDependencies and start the server.

```sh
cd dillinger
npm i
node app
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
```

## Plugins

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

## Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantaneously see your updates!

Open your favorite Terminal and run these commands.

First Tab:

```sh
node app
```

Second Tab:

```sh
gulp watch
```

(optional) Third:

```sh
karma test
```

#### Building for source

For production release:

```sh
gulp build --prod
```

Generating pre-built zip archives for distribution:

```sh
gulp build dist --prod
```

## Docker

Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

```sh
cd dillinger
docker build -t <youruser>/dillinger:${package.json.version} .
```

This will create the dillinger image and pull in the necessary dependencies.
Be sure to swap out `${package.json.version}` with the actual
version of Dillinger.

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 8000 of the host to
port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart=always --cap-add=SYS_ADMIN --name=dillinger <youruser>/dillinger:${package.json.version}
```

> Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
