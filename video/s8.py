import random

from common import *


class S8(VScene):
    def construct(self):
        self.session_title(
            8, "Streaming Video at Large Scale", "One live cricket match on fifty million phones",
            "Session eight. Streaming video at large scale. It starts with a live cricket scorecard. "
            "And by the end you will see that every live stream is a scorecard with bigger bytes.")
        self.ch_hook()
        self.ch_brief()
        self.ch_families()
        self.ch_polling()
        self.ch_longpoll()
        self.ch_sse()
        self.ch_websocket()
        self.ch_mqtt()
        self.ch_hotstar()
        self.ch_socket_cost()
        self.ch_little()
        self.ch_arithmetic()
        self.ch_four_bills()
        self.ch_per_request()
        self.ch_conditional()
        self.ch_ttls()
        self.ch_herd()
        self.ch_negative()
        self.ch_diffs()
        self.ch_hls_picture()
        self.ch_master()
        self.ch_media_playlist()
        self.ch_mpegts()
        self.ch_segment_len()
        self.ch_buffer()
        self.ch_latency()
        self.ch_spoiler()
        self.ch_abr()
        self.ch_multicdn()
        self.ch_stale_404()
        self.ch_ffmpeg()
        self.ch_course()
        self.ch_four_ideas()
        self.quiz()

    # ------------------------------------------------------------------
    def ch_hook(self):
        self.new_slide("Every live stream is a scorecard with bigger bytes", "Look at three requests from the same app, during the same match.", C_YELLOW)
        rows = [("GET /match/412/score.json", "200 · 1,088 B · every 15 s", C_BLUE),
                ("GET /stream_1/index.m3u8", "200 · 228 B · every 4 s", C_PURPLE),
                ("GET /stream_1/seg_000008.ts", "200 · 823,440 B · once", C_GREEN)]
        nars = ["The scorecard. A thousand and eighty-eight bytes, fetched every fifteen seconds.",
                "A video playlist. Two hundred twenty-eight bytes, fetched every four seconds.",
                "And a video segment. Eight hundred twenty-three thousand bytes, fetched exactly once."]
        g = VGroup()
        for i, ((a, b, c), n) in enumerate(zip(rows, nars)):
            r = VGroup(M(a, 24, c, maxw=6.6), T(b, 22, C_GREY, maxw=5.4)).arrange(RIGHT, buff=0.6)
            r.move_to([0, 1.3 - i * 1.0, 0])
            with self.vo(n):
                self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.6)
            g.add(r)
        t = T("Same loop: poll a small index, fetch numbered pieces. All 8 weeks show up in one system.", 24, C_YELLOW, maxw=12.4).shift(DOWN * 2.2)
        with self.vo("It is the same loop each time: poll something small, then fetch numbered pieces. Every week of this course shows up in this one system: one live match, on fifty million phones."):
            self.play(FadeIn(t))

    def ch_brief(self):
        self.new_slide("The brief", "Here is the brief.", C_BLUE)
        items = [("25-45 s", "between balls; an over every 4-5 min", C_BLUE),
                 ("50 M", "peak concurrent viewers", C_RED),
                 ("20 M", "average, over a 4-hour match", C_ORANGE),
                 ("~1 KB", "scorecard JSON gzipped (4-5 KB raw)", C_GREEN),
                 ("100", "events a year", C_PURPLE)]
        nars = ["Twenty-five to forty-five seconds between balls. An over every four or five minutes.",
                "Fifty million concurrent viewers at the peak.",
                "Twenty million on average, over a four-hour match.",
                "The scorecard is four to five kilobytes of JSON, about one kilobyte gzipped.",
                "And a hundred events like this every year."]
        cards = VGroup()
        for (big, small, c) in items:
            cards.add(VGroup(T(big, 40, c), T(small, 18, C_GREY, maxw=2.3)).arrange(DOWN, buff=0.25))
        cards.arrange(RIGHT, buff=0.55).shift(UP * 0.2)
        if cards.width > 12.8:
            cards.scale(12.8 / cards.width)
        for cd, n in zip(cards, nars):
            with self.vo(n):
                self.play(FadeIn(cd, shift=UP * 0.2), run_time=0.6)

    def ch_families(self):
        self.new_slide("Two families of delivery", "There are two families of delivery. Either the client asks, or the server tells.", C_YELLOW)
        L = VGroup(T("Non-persistent: the client asks", 26, C_GREEN),
                   *[T(s, 21, WHITE, maxw=5.8) for s in ["Polling: GET the same URL every few s", "Conditional GET: 304 when nothing changed", "Caches: nginx, then a CDN", "any server, no memory of who asked"]]
                   ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([-3.4, 0.6, 0])
        R = VGroup(T("Persistent: the server tells", 26, C_ORANGE),
                   *[T(s, 21, WHITE, maxw=5.8) for s in ["Long poll: GET answered only on news", "Server-Sent Events: a never-ending response", "WebSockets: a two-way framed pipe", "Pub/Sub (MQTT): topics, broker, fan-out", "a plain binary socket of your own"]]
                   ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([3.4, 0.5, 0])
        with self.vo("On the left, non-persistent. Polling, conditional GETs that come back three oh four, and caches, first nginx, then a CDN. Any server can answer, and nobody remembers who asked."):
            self.play(FadeIn(L, lag_ratio=0.15), run_time=1.5)
        with self.vo("On the right, persistent. Long polling, server-sent events, WebSockets, publish subscribe with MQTT, or your own binary protocol on a socket."):
            self.play(FadeIn(R, lag_ratio=0.15), run_time=1.5)
        b1 = T("ordinary GETs -> stateless, cacheable, a CDN can front it", 21, C_GREEN, maxw=6.0).move_to([-3.4, -2.6, 0])
        b2 = T("a connection per viewer, all match -> stateful, nothing to cache", 21, C_ORANGE, maxw=6.0).move_to([3.4, -2.6, 0])
        with self.vo("That is the whole trade. Polling is ordinary GETs: stateless servers, cacheable, a CDN can sit in front. Push means every viewer holds a connection for the whole match: stateful servers, and nothing a CDN can cache."):
            self.play(FadeIn(b1), FadeIn(b2))

    def ch_polling(self):
        self.new_slide("Polling, done properly", "Polling first. Done properly, it is about seven lines.", C_GREEN)
        code = self.code_block(["let etag = null; const EVERY = 15_000;",
                                "async function poll() {",
                                "  const res = await fetch(\"/match/412/score.json\",",
                                "      { headers: etag ? { \"If-None-Match\": etag } : {} });",
                                "  if (res.status === 200) { etag = res.headers.get(\"ETag\"); render(await res.json()); }",
                                "  const jitter = 0.8 + Math.random() * 0.4;   // +/-20%",
                                "  setTimeout(poll, EVERY * jitter);",
                                "}"], size=18, pos=UP * 0.7, hl={"If-None-Match": C_YELLOW, "ETag": C_YELLOW, "jitter": C_ORANGE})
        if code.width > 13:
            code.scale(13 / code.width)
        with self.vo("Remember the ETag. Send it back in If-None-Match. On a two hundred, render the new card. On a three oh four, keep what you have: an empty body, but the request still happens."):
            self.play(FadeIn(code))
        random.seed(8)
        ax = Line([-6, -2.6, 0], [6, -2.6, 0], color=C_GREY)
        bad = VGroup(*[Dot([-3.0 + 0.03 * random.random(), -2.4 + 0.12 * k, 0], radius=0.05, color=C_RED) for k in range(8)])
        good = VGroup(*[Dot([random.uniform(0.5, 5.8), -2.4 + 0.12 * random.randint(0, 2), 0], radius=0.05, color=C_GREEN) for _ in range(24)])
        with self.vo("Then the jitter: plus or minus twenty percent. Without it, fifty million phones poll in the same second."):
            self.play(Create(ax), FadeIn(bad, lag_ratio=0.1))
        with self.vo("With it, they spread out. And the freshness you can promise, at worst, is one poll interval plus every cache TTL on the path."):
            self.play(FadeIn(good, lag_ratio=0.05), run_time=1.5)

    def ch_longpoll(self):
        self.new_slide("Long polling: a GET answered only when there's news", "Long polling. The server holds the GET until there is news.", C_ORANGE)
        ll = self.lifelines("Phone", "Server", x=3.2, y_top=1.8)
        self.msg(ll, "r", "GET /score?after=1841", C_YELLOW, dy=0.9, size=20, note="server holds... up to 25 s", narration="The phone asks for anything after version eighteen forty-one. The server holds the request until ball eighteen forty-two happens, or twenty-five seconds pass.")
        self.msg(ll, "l", '200 {"version":1842,...}', C_GREEN, dy=0.9, size=20, narration="Then it answers, and the phone asks again immediately.")
        self.msg(ll, "r", "GET /score?after=1842", C_YELLOW, dy=0.9, size=20)
        pts = [("A held request is a held socket: W is 25 s, not 30 ms (Little's Law)", "A held request is a held socket. In Little's Law, W is now twenty-five seconds, not thirty milliseconds."),
               ("Answer before the idle timeouts: nginx proxy_read_timeout and ALB idle both default 60 s", "Answer before the idle timeouts. nginx proxy read timeout and the A W S load balancer idle timeout both default to sixty seconds."),
               ("It synchronises the herd: a wicket completes 20 M responses in 1 s -> 20 M requests the next second", "And it synchronises the herd. A wicket completes twenty million responses in one second, so twenty million new requests arrive the next second."),
               ("It came back standardised: LL-HLS blocking playlist reload = long polling", "Keep it in mind, because it comes back standardised: Low-Latency HLS's blocking playlist reload is long polling.")]
        self.bullets(pts, size=20, gap=0.22, shift=DOWN * 2.15)

    def ch_sse(self):
        self.new_slide("Server-Sent Events: one response that never ends", "Server-Sent Events. One response that never ends.", C_TEAL)
        code = self.code_block(["GET /match/412/events   Accept: text/event-stream   Last-Event-ID: 1841",
                                "HTTP/1.1 200 OK   Content-Type: text/event-stream",
                                "retry: 5000", "",
                                "id: 1842", "event: ball", "data: {\"over\":\"15.4\",\"runs\":4,\"total\":\"146/4\"}",
                                "<blank line = end of event>"], size=19, pos=UP * 0.8, hl={"Last-Event-ID": C_YELLOW, "retry:": C_ORANGE, "<blank line = end of event>": C_RED})
        with self.vo("The request asks for text slash event stream. The response is a two hundred that simply never finishes. Each event has an id, a type, and data, and ends at a blank line."):
            self.play(FadeIn(code))
        pts = [("Framing by delimiter: a blank line ends an event - SMTP's lone dot in another costume", "That is framing by delimiter. SMTP's lone dot, in another costume."),
               ("Resume: on reconnect the browser sends Last-Event-ID; the server replays only what was missed. retry: sets the delay", "To resume, the browser sends Last-Event-ID when it reconnects, and the server replays only what was missed. The retry field sets the reconnect delay."),
               ("~6 per browser on HTTP/1.1 (each tab its own connection); HTTP/2 multiplexes them. One way only", "About six per browser over HTTP one point one, since each tab holds its own connection. HTTP two multiplexes them. And it is one way only, server to client.")]
        self.bullets(pts, size=20, gap=0.25, shift=DOWN * 2.0)

    def ch_websocket(self):
        self.new_slide("WebSockets: HTTP upgrades into a framed pipe", "WebSockets. HTTP upgrades itself into a two-way framed pipe.", C_PURPLE)
        ll = self.lifelines("Browser", "Server", x=3.2, y_top=2.0)
        self.msg(ll, "r", "GET /live  Upgrade: websocket", C_YELLOW, dy=0.85, size=19, note="Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==", narration="The browser sends an ordinary GET with Upgrade websocket and a random key.")
        self.msg(ll, "l", "101 Switching Protocols", C_GREEN, dy=0.85, size=19, note="Accept = base64( SHA-1( key + fixed GUID ) )", narration="The server answers one oh one, Switching Protocols. The Accept header is base sixty-four of the SHA one of the key plus a fixed GUID. Week one's base sixty-four, showing up again.")
        frame = VGroup(*[box(l, c, w=w, h=0.7, size=17) for l, c, w in
                         [("FIN·RSV·opcode", C_BLUE, 2.3), ("MASK·len 0-125", C_ORANGE, 2.3), ("ext len 0/2/8 B", C_YELLOW, 2.3), ("mask key 4 B", C_RED, 2.0), ("payload", C_GREEN, 2.6)]]
                       ).arrange(RIGHT, buff=0.05).move_to([0, -2.0, 0])
        with self.vo("After that, everything is frames. Byte one holds FIN and the opcode: text, binary, ping, pong, close. Byte two holds the mask bit and a length. One twenty-six means a sixteen-bit length follows, one twenty-seven means sixty-four bits. Length-prefixed, not delimited: the other framing answer."):
            self.play(FadeIn(frame, lag_ratio=0.2), run_time=2)
        t = T("Client frames are always masked, so stray bytes never look like a request to a caching proxy.", 20, C_RED, maxw=12.4).next_to(frame, DOWN, buff=0.35)
        with self.vo("And every frame from the client is masked with a four-byte key, so stray bytes can never look like a request to a caching proxy. That is a cache poisoning defence."):
            self.play(FadeIn(t))

    def ch_mqtt(self):
        self.new_slide("MQTT: publish once, fan out", "MQTT. Publish once, and the broker fans it out.", C_BLUE)
        pub = box("Publisher", C_ORANGE, w=2.4).move_to([-5.0, 0.6, 0])
        brk = box("Broker\n(retains last score)", C_BLUE, w=3.2, h=1.3, size=22).move_to([-0.8, 0.6, 0])
        phones = VGroup(*[box(f"phone {i}", C_GREEN, w=1.8, h=0.6, size=18) for i in range(1, 6)]).arrange(DOWN, buff=0.15).move_to([4.6, 0.6, 0])
        a1 = Arrow(pub.get_right(), brk.get_left(), color=C_ORANGE, buff=0.1)
        lab = M("PUBLISH match/412/score retain=1", 18, C_ORANGE).next_to(VGroup(pub, brk), UP, buff=0.3).align_to(pub, LEFT)
        with self.vo("Phones connect with a keepalive, and subscribe to a topic: match slash four twelve slash score. The publisher sends one message."):
            self.play(FadeIn(pub), FadeIn(brk), FadeIn(phones))
            self.play(GrowArrow(a1), FadeIn(lab))
        arrs = VGroup(*[Arrow(brk.get_right(), p.get_left(), color=C_GREEN, buff=0.1, stroke_width=3) for p in phones])
        with self.vo("The broker copies it to every subscriber. And because it is a retained message, the broker keeps the last score and hands it to every new subscriber immediately. A cache, inside the broker."):
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.15))
        pts = [("QoS 1 = at-least-once -> duplicates happen; apply updates by version number", "Quality of service one is at least once, so duplicates happen. Apply updates by version number and duplicates are harmless."),
               ("PINGREQ C0 00 / PINGRESP D0 00: two bytes each keepalive - keeps the NAT mapping alive (and wakes the radio)", "Keepalives are two bytes each way: C zero zero, and D zero zero. They keep the NAT mapping alive, and wake the phone's radio."),
               ("Remaining Length is a varint: 7 bits per byte, top bit = more", "And the remaining length is a varint: seven bits per byte, the top bit says more is coming.")]
        self.bullets(pts, size=20, gap=0.22, shift=DOWN * 2.3)

    def ch_hotstar(self):
        self.new_slide("How Hotstar held 50 million sockets (2019)", "How Hotstar held fifty million sockets, from their engineering blog in June twenty nineteen. They chose MQTT with the EMQX broker.", C_RED)
        self.bars([("1 node (c5.4xlarge)", 0.25, C_BLUE), ("cluster, pub split from subs", 2, C_TEAL), ("pre-warmed Classic ELB", 4, C_YELLOW), ("5 bridged clusters", 10, C_ORANGE), ("reverse bridge, 200 nodes", 50, C_RED)],
                  50, y0=1.7, gap=0.85, left=-1.2, width=7.0, label_w=4.6, size=21, unit=" M",
                  narrs=["One EMQX node on a c five four x large: two hundred fifty thousand connections.",
                         "A cluster, with the publisher split from the subscribers: two million. The Mnesia database wants fewer than ten nodes.",
                         "Then the load balancer wall. An ELB drops at about half a million without pre-warming. Four million per pre-warmed classic ELB.",
                         "Five clusters of eight subscribe nodes, bridged together: past ten million.",
                         "And a reverse bridge: a Go service on each subscriber pulls from the publisher. Two hundred nodes, fifty million."])
        t = T("Their social feed was per-user and tied to live moments - 'caching at any level is not possible'. A scorecard is the opposite.", 20, C_GREY, maxw=12.4).to_edge(DOWN, buff=0.4)
        with self.vo("Why push? Their social feed was different for every user and tied to live moments. Caching at any level was not possible. A scorecard is the opposite: one file, identical for everyone."):
            self.play(FadeIn(t))

    def ch_socket_cost(self):
        self.new_slide("What a held socket costs", "So what does a held socket actually cost?", C_ORANGE)
        tbl = self.table([["Cost", "What it means"],
                          ["Machines", "stateful: a phone lives on one box for hours; 100-200k per box; rebalancing = disconnecting people"],
                          ["Memory", "socket buffers, TLS state, per-client process: 250k on 32 GiB = ~137 KB each"],
                          ["Network", "60 s keepalive x 20 M idle phones = 333k pings/s before the first ball"],
                          ["Load balancers", "the LB holds every socket too (4 M per Classic ELB)"],
                          ["Testing", "28,232 ephemeral ports per client IP -> 250k sockets need >= 9 source IPs"]],
                         [2.6, 10.2], size=20, y=0.5, row_h=0.9)
        self.reveal_rows(tbl, ["Machines. Each phone lives on one box for hours. A hundred to two hundred thousand per box. New boxes sit empty until people reconnect, so rebalancing means disconnecting people.",
                               "Memory. Kernel buffers, TLS state, a broker process per client. Two hundred fifty thousand phones on thirty-two gigabytes is about a hundred thirty-seven kilobytes each.",
                               "Network. A sixty-second keepalive across twenty million idle phones is three hundred thirty-three thousand pings a second, before the first ball is bowled.",
                               "Load balancers hold every socket too.",
                               "And testing. One client IP has twenty-eight thousand two hundred thirty-two ephemeral ports per destination. Week one's sixteen-bit ports. So two hundred fifty thousand test sockets need at least nine source IPs."])

    def ch_little(self):
        self.new_slide("Little's Law, twice:  L = λ × W", "Little's Law, twice. L equals lambda times W.", C_YELLOW)
        L = VGroup(T("Polling through a CDN", 26, C_GREEN), T("1.67 M req/s × 0.03 s", 26), T("= 50,000 in flight", 30, C_GREEN)).arrange(DOWN, buff=0.3).move_to([-3.4, 0.8, 0])
        R = VGroup(T("Push over held sockets", 26, C_ORANGE), T("W = the whole match (4 h)", 26), T("= 50,000,000 held", 30, C_ORANGE)).arrange(DOWN, buff=0.3).move_to([3.4, 0.8, 0])
        with self.vo("Polling through a CDN: one point six seven million requests a second, each spending about thirty milliseconds at the edge. Fifty thousand in flight."):
            self.play(FadeIn(L, lag_ratio=0.2))
        with self.vo("Push: W is the whole match, four hours. Fifty million sockets held."):
            self.play(FadeIn(R, lag_ratio=0.2))
        sq1 = Square(0.12, color=C_GREEN, fill_opacity=1).move_to([-3.4, -1.9, 0])
        sq2 = Square(3.8, color=C_ORANGE, fill_opacity=0.5).move_to([3.4, -1.9, 0]).scale(0.5)
        t = T("1000× the concurrency, same audience - because W went from ms to hours", 24, C_YELLOW, maxw=12.4).to_edge(DOWN, buff=0.3)
        with self.vo("A thousand times the concurrency for the same audience. Only because W went from milliseconds to hours."):
            self.play(FadeIn(sq1), GrowFromCenter(sq2), FadeIn(t))

    def ch_arithmetic(self):
        self.new_slide("The arithmetic before the architecture", "Do the arithmetic before you draw the architecture. Polling every thirty seconds.", C_BLUE)
        lines = [("requests / match", "20 M × 14,400 s ÷ 30 s", "= 9.6 B", "Twenty million viewers, fourteen thousand four hundred seconds, one request every thirty. Nine point six billion requests a match."),
                 ("peak rate", "50 M ÷ 30 s", "= 1.67 M req/s", "Peak rate: fifty million over thirty seconds. One point six seven million requests a second."),
                 ("bytes / match", "9.6 B × 1 KB", "= 9.6 TB", "Bytes: nine point six terabytes a match."),
                 ("poll every 15 s", "double everything", "= 19.2 B, 3.33 M/s", "Poll every fifteen seconds and everything doubles."),
                 ("× 100 events", "per year", "= 960 B req, 960 TB", "Times a hundred events: nine hundred sixty billion requests a year.")]
        for i, (a, b, c, n) in enumerate(lines):
            r = VGroup(T(a, 24, C_BLUE, maxw=3.5), T(b, 24, WHITE, maxw=4.6), T(c, 26, C_YELLOW, maxw=4.0))
            for m, x in zip(r, [-6.2, -2.4, 2.6]):
                m.move_to([x + m.width / 2, 1.6 - i * 0.95, 0])
            with self.vo(n):
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)

    def ch_four_bills(self):
        self.new_slide("Four ways to pay for one match", "Four ways to pay for one match, at A W S list prices.", C_GREEN)
        self.bars([("S3 straight to phones", 4.7, C_ORANGE), ("nginx fleet + ALB", 1.5, C_BLUE), ("CDN (CloudFront India)", 12.5, C_RED), ("Push: 200 × c5.4xlarge", 1.25, C_GREEN)],
                  12.5, y0=1.6, gap=0.95, left=-1.0, width=6.6, label_w=4.6, size=22, unit=" K$",
                  narrs=["S3 straight to phones: about four point seven thousand dollars, mostly G E T fees. It breaks first on the request rate limit.",
                         "An nginx fleet behind a load balancer: twelve to eighteen hundred dollars, mostly egress. It breaks on twenty to fifty million idle keep-alive sockets at the load balancer.",
                         "Through a CDN: twelve and a half thousand dollars. Ninety-two percent of it is request fees. Nothing breaks. It is just the bill.",
                         "And push on two hundred servers: nine hundred to sixteen hundred dollars. It breaks on reconnect storms and rebalancing."])
        t = T("At list price: push is cheapest per match, the CDN dearest.", 24, C_YELLOW).to_edge(DOWN, buff=0.5)
        with self.vo("So at list price, push is the cheapest per match, and the CDN is the dearest."):
            self.play(FadeIn(t))
        self.new_slide("S3 runs out of requests before money", "And S3 runs out of requests before it runs out of money.", C_RED)
        self.bars([("S3 promise / prefix", 5.5, C_GREEN), ("50 M phones / 30 s", 1670, C_RED)], 1670, y0=1.0, gap=1.2, left=-2.2, width=5.6, label_w=4.4, size=22, unit=" K GET/s",
                  narrs=["S3 promises at least fifty-five hundred GETs a second per prefix.", "Fifty million phones polling every thirty seconds ask for one point six seven million. Three hundred and three times over."])
        t = T("'You may see some 503 Slow Down errors' -> 50 M clients retrying = Session 7's retry storm", 22, C_ORANGE, maxw=12.4).shift(DOWN * 1.8)
        with self.vo("The documentation says: you may see some five oh three Slow Down errors. Fifty million clients retrying without backoff is session seven's retry storm, aimed at your own bucket."):
            self.play(FadeIn(t))

    def ch_per_request(self):
        self.new_slide("Billed per request, or per byte?", "Why is the CDN so expensive here? Because you are billed per request and per byte.", C_PURPLE)
        ax = Axes(x_range=[0, 30, 5], y_range=[0, 3.5, 1], x_length=9, y_length=3.6, axis_config={"color": C_GREY, "include_ticks": False}).shift(UP * 0.1 + LEFT * 0.3)
        req = ax.plot(lambda x: 1.2, color=C_ORANGE)
        byt = ax.plot(lambda x: 0.109 * x, color=C_BLUE)
        xl = T("object size (KB)", 18, C_GREY).next_to(ax, DOWN, buff=0.1)
        yl = T("$ per million", 18, C_GREY).next_to(ax, LEFT, buff=0.1).rotate(PI / 2)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
        with self.vo("CloudFront in India charges one dollar twenty per million HTTPS requests, whatever the size."):
            self.play(Create(req), FadeIn(T("request fee $1.20", 18, C_ORANGE).next_to(ax.c2p(30, 1.2), UP + LEFT * 0.2, buff=0.1)))
        with self.vo("And about eleven cents per gigabyte. That line grows with the size of the object."):
            self.play(Create(byt), FadeIn(T("bytes $0.109/GB", 18, C_BLUE).next_to(ax.c2p(28, 3.05), LEFT, buff=0.1)))
        d = Dot(ax.c2p(11, 1.2), color=C_YELLOW, radius=0.1)
        lab = T("break-even ≈ 11 KB", 22, C_YELLOW).next_to(d, UP, buff=0.4)
        with self.vo("They cross at about eleven kilobytes. Below it you pay per request: the one-kilobyte scorecard, the two hundred twenty-eight byte playlist. Ninety-two percent of the scorecard's bill is request fees. Above it you pay per byte: video segments."):
            self.play(FadeIn(d), FadeIn(lab))
        t = T("Why the lecturer still prefers polling: cacheable · stateless · already paid for (0.28% of the video bill)", 21, C_GREEN, maxw=12.4).to_edge(DOWN, buff=0.35)
        with self.vo("So why prefer polling anyway? It is cacheable, one file identical for fifty million. It is stateless, any edge can answer. And it is already paid for: the scorecard is zero point two eight percent of the match's video bill. And, as you will see, it is exactly how video works."):
            self.play(FadeIn(t))

    def ch_conditional(self):
        self.new_slide("Making polling survive: conditional GET", "Now, making polling survive. First, the conditional GET.", C_GREEN)
        ll = self.lifelines("Phone / edge", "Origin", x=3.2, y_top=1.8)
        self.msg(ll, "r", 'If-None-Match: "v1841"', C_YELLOW, dy=0.9, size=20, narration="The ETag is the scorecard's version number. A fingerprint, not a clock. If-Modified-Since only resolves to the second.")
        self.msg(ll, "l", '304 Not Modified  ETag: "v1841"', C_GREEN, dy=0.9, size=20, note="Cache-Control: public, max-age=10", narration="Nothing changed, so three oh four, with Cache-Control public, max age ten.")
        L = T("Saves: the 1 KB body, the JSON parse, the re-render", 22, C_GREEN).move_to([0, -1.6, 0])
        R = T("Doesn't save: the request fee, the round trip, the headers", 22, C_RED).move_to([0, -2.2, 0])
        with self.vo("It saves the body, the parse and the re-render. It does not save the request fee, the round trip, or the headers."):
            self.play(FadeIn(L), FadeIn(R))
        t = T("It pays most between CDN tiers: edge -> mid-tier -> origin exchange 304s, not copies.", 21, C_YELLOW, maxw=12.4).to_edge(DOWN, buff=0.3)
        with self.vo("Where it pays most is between CDN tiers. The edge, the mid-tier and the origin exchange three oh fours instead of copies."):
            self.play(FadeIn(t))

    def ch_ttls(self):
        self.new_slide("TTLs add up", "Here is a trap: TTLs add up.", C_ORANGE)
        def stack(parts, y, label, col):
            g = VGroup()
            x = -4.0
            for name, s, c in parts:
                r = Rectangle(width=s * 0.09, height=0.6, color=c, fill_opacity=0.6).move_to([x + s * 0.045, y, 0])
                t = T(f"{name} {s}s", 16, WHITE, maxw=s * 0.09 - 0.05).move_to(r)
                g.add(VGroup(r, t))
                x += s * 0.09
            tot = T(label, 22, col).next_to(g, RIGHT, buff=0.3)
            return VGroup(g, tot)
        a = stack([("mid-tier", 30, C_BLUE), ("edge", 30, C_PURPLE), ("poll", 30, C_ORANGE)], 1.2, "up to 90 s stale", C_RED).shift(LEFT * 1.2)
        b = stack([("mid", 5, C_BLUE), ("edge", 5, C_PURPLE), ("poll", 15, C_ORANGE)], -0.2, "up to 25 s", C_GREEN).shift(LEFT * 1.2)
        with self.vo("Thirty seconds at the mid-tier, thirty at the edge, and a thirty-second poll. Up to ninety seconds stale. Two or three balls behind."):
            self.play(FadeIn(a, lag_ratio=0.3), run_time=1.5)
        with self.vo("CDN TTLs of five and five, with a fifteen-second poll: up to twenty-five seconds. Inside one ball."):
            self.play(FadeIn(b, lag_ratio=0.3), run_time=1.5)
        pts = [("Worst-case staleness = poll interval + every cache TTL on the path", "Worst-case staleness is the poll interval plus every cache TTL on the path."),
               ("Keep each CDN TTL <= half your promised freshness; refresh before expiry (Akamai 'prefresh' at ~25 s of 30)", "So keep each CDN TTL at most half of what you promise, and refresh before expiry. Akamai calls it prefresh: refetch at twenty-five seconds of a thirty-second TTL.")]
        self.bullets(pts, size=21, gap=0.3, shift=DOWN * 2.2)

    def ch_herd(self):
        self.new_slide("The thundering herd at expiry", "When a popular object expires, everyone misses at once. The thundering herd.", C_RED)
        edge = box("edge", C_BLUE, w=2.0).move_to([0, 0.8, 0])
        org = box("origin", C_ORANGE, w=2.0).move_to([4.6, 0.8, 0])
        random.seed(2)
        phones = VGroup(*[Dot([random.uniform(-6.3, -3.6), random.uniform(-0.6, 2.2), 0], radius=0.06, color=C_GREEN) for _ in range(40)])
        arrs = VGroup(*[Line(p.get_center(), edge.get_left(), color=C_GREEN, stroke_width=1, stroke_opacity=0.5) for p in phones])
        with self.vo("Twenty thousand phones ask one edge for the same object in the same fifty milliseconds."):
            self.play(FadeIn(edge), FadeIn(org), FadeIn(phones, lag_ratio=0.02), Create(arrs, lag_ratio=0.02), run_time=1.5)
        one = Arrow(edge.get_right(), org.get_left(), color=C_YELLOW, buff=0.1)
        with self.vo("With request collapsing, the edge sends one request upstream, and the origin sees one. The rest queue."):
            self.play(GrowArrow(one), FadeIn(T("1 request", 20, C_YELLOW).next_to(one, UP, buff=0.1)))
        code = self.code_block(["proxy_cache_lock on;",
                                "proxy_cache_use_stale updating error timeout http_500 http_502 http_503 http_504;",
                                "proxy_cache_background_update on;",
                                "proxy_cache_valid 200 10s;"], size=18, pos=DOWN * 1.6)
        if code.width > 13:
            code.scale(13 / code.width)
        with self.vo("Four fixes. One, request collapsing: proxy cache lock. Two, serve stale while updating, R F C fifty-eight sixty-one. Three, prefetch before expiry. Four, jitter from the client."):
            self.play(FadeIn(code))
        t = T("Collapsing needs a shareable answer: public releases every waiter; a private answer or a stray Set-Cookie dequeues them one by one.", 19, C_ORANGE, maxw=12.6).to_edge(DOWN, buff=0.25)
        with self.vo("But collapsing needs a shareable answer. Cache-Control public releases every waiter at once. A private answer, or a stray Set-Cookie, dequeues them one by one, and Fastly then skips collapsing for that object for two minutes. Also check defaults: Cloudflare does not cache dot json out of the box, so every poll reaches you."):
            self.play(FadeIn(t))

    def ch_negative(self):
        self.new_slide("Negative caching", "Negative caching. Should you cache errors?", C_PURPLE)
        L = VGroup(T("5xx: cache it briefly", 28, C_GREEN), T("1-2 s of a cached 503 shields a", 22), T("struggling origin from 50 M retries:", 22), T("one probe per TTL per edge", 22, C_GREEN)).arrange(DOWN, buff=0.2).move_to([-3.4, 1.0, 0])
        R = VGroup(T("404: almost never", 28, C_RED), T("a 404 for a file about to exist", 22), T("(newest live segment, next match)", 22), T("Cloudflare default 404 TTL = 3 min", 22, C_RED)).arrange(DOWN, buff=0.2).move_to([3.4, 1.0, 0])
        with self.vo("Five hundreds: yes, briefly. One or two seconds of a cached five oh three shields a struggling origin from fifty million retries. Each edge sends one probe per TTL."):
            self.play(FadeIn(L))
        with self.vo("Four oh fours: almost never. A four oh four for a file that is about to exist, like the newest live segment, keeps being served after the file appears. Cloudflare's default four oh four TTL is three minutes."):
            self.play(FadeIn(R))
        t = T("Rule: a negative TTL must be far shorter than the time the missing thing takes to appear.", 23, C_YELLOW, maxw=12.4).shift(DOWN * 1.8)
        with self.vo("The rule: a negative TTL must be far shorter than the time the missing thing takes to appear."):
            self.play(FadeIn(t))

    def ch_diffs(self):
        self.new_slide("Send diffs, not the whole card", "Send diffs, not the whole card.", C_TEAL)
        self.bars([("full JSON", 4117, C_RED), ("gzipped", 1088, C_ORANGE), ("JSON Patch, gzipped", 183, C_GREEN)], 4117, y0=2.0, gap=0.9, left=-1.5, width=6.5, label_w=4.0, size=22, unit=" B",
                  narrs=["The full card is four thousand one hundred seventeen bytes.", "Gzipped, a thousand and eighty-eight.", "One ball, as a gzipped JSON Patch: one hundred eighty-three bytes."])
        pts = [("Push: SSE / MQTT carry the 183-byte patch; a phone that sees a version gap fetches the full card once", "With push, the patch rides on SSE or MQTT. A phone that sees a gap in version numbers fetches the full card once."),
               ("Pull: ?since=1841 gives every client its own URL -> hit rate collapses. Publish ONE file: version + last few changes", "With pull, a since parameter gives every client its own URL, and the hit rate collapses. Instead, publish one file with the version and the last few changes.")]
        self.bullets(pts, size=21, gap=0.3, shift=DOWN * 1.4)
        self.new_slide("A versioned scorecard IS a playlist", "And now look what we have built.", C_YELLOW)
        tbl = self.table([["score.json (polled 15 s)", "index.m3u8 (polled 4 s)"],
                          ["version", "#EXT-X-MEDIA-SEQUENCE"],
                          ["recent changes", "the last N segments"],
                          ["poll interval", "#EXT-X-TARGETDURATION"]], [5.5, 5.5], size=26, y=0.8, row_h=0.9)
        self.reveal_rows(tbl, ["The version number is the media sequence.", "The recent changes are the last few segments.", "The poll interval is the target duration."])
        t = T("A small index everyone polls, pointing at numbered pieces that never change: HTTP Live Streaming (HLS).", 23, C_GREEN, maxw=12.4).to_edge(DOWN, buff=0.6)
        with self.vo("A small index that everyone polls, pointing at numbered pieces that never change. That design has a name: HTTP Live Streaming. H L S."):
            self.play(FadeIn(t))

    def ch_hls_picture(self):
        self.new_slide("HLS in one picture: control vs data", "H L S in one picture. Control, and data.", C_BLUE)
        _, bx = self.flow(["master.m3u8\nonce", "stream_1/index.m3u8\nevery 4 s", "seg_000011.ts\neach new one", "player buffer\n-> screen"],
                          [C_PURPLE, C_BLUE, C_GREEN, C_ORANGE], y=0.8, w=3.0, h=1.3, size=20, gap=0.35,
                          narrations=["The master playlist, fetched once. A menu of renditions: bandwidth, resolution, codecs. That is control.",
                                      "The media playlist for the chosen rendition, re-fetched every target duration, four seconds. It lists the last ten segments. Also control.",
                                      "Each new segment: four seconds of audio and video, eight hundred twenty-three kilobytes, and it never changes. That is data.",
                                      "The player plays from its buffer, and switches rendition when throughput changes."])
        c = Brace(VGroup(bx[0], bx[1]), DOWN, color=C_BLUE)
        d = Brace(VGroup(bx[2]), DOWN, color=C_GREEN)
        self.play(FadeIn(c), FadeIn(T("CONTROL: small, changing", 20, C_BLUE).next_to(c, DOWN)), FadeIn(d), FadeIn(T("DATA: big, immutable", 20, C_GREEN).next_to(d, DOWN)))
        self.wait(1.5)

    def ch_master(self):
        self.new_slide("The master playlist", "The master playlist.", C_PURPLE)
        code = self.code_block(["#EXTM3U", "#EXT-X-VERSION:6",
                                "#EXT-X-STREAM-INF:BANDWIDTH=3440800,RESOLUTION=1280x720,CODECS=\"avc1.4d401f,mp4a.40.2\"", "stream_0/index.m3u8",
                                "#EXT-X-STREAM-INF:BANDWIDTH=1755600,RESOLUTION=854x480,CODECS=\"avc1.4d401f,mp4a.40.2\"", "stream_1/index.m3u8",
                                "#EXT-X-STREAM-INF:BANDWIDTH=950400,RESOLUTION=640x360,CODECS=\"avc1.4d401e,mp4a.40.2\"", "stream_2/index.m3u8"],
                               size=17, pos=UP * 0.9, hl={"BANDWIDTH": C_YELLOW, "CODECS": C_GREEN})
        if code.width > 13:
            code.scale(13 / code.width)
        with self.vo("Three renditions: seven twenty p, four eighty p, three sixty p. Each with a bandwidth, a resolution, and codecs."):
            self.play(FadeIn(code))
        pts = [("BANDWIDTH = (video + audio) × 1.1:  (3000k + 128k) × 1.1 = 3,440,800", "Bandwidth is video plus audio, times one point one. Three thousand k plus one twenty-eight k, times one point one, is three million four hundred forty thousand eight hundred."),
               ("Doesn't change during the match: fetch once. Some players re-poll it to switch CDNs -> Content Steering", "It does not change during the match, so fetch once and cache it for minutes. Some players re-poll it to switch CDNs, which got standardised as Content Steering."),
               ("CODECS lets the player skip what it can't decode (HEVC -> H.264): a fallback, not a retry", "And CODECS lets the player skip what it cannot decode, say HEVC, and pick H.264. That is a fallback, not a retry. a v c one is H.264, m p four a is A A C.")]
        self.bullets(pts, size=20, gap=0.25, shift=DOWN * 2.0)

    def ch_media_playlist(self):
        self.new_slide("The media playlist, polled (RFC 8216 §6.3.4)", "The media playlist slides forward like a window.", C_BLUE)
        segs = VGroup(*[box(f"{i:02d}", C_GREEN, w=0.95, h=0.7, size=20) for i in range(0, 14)]).arrange(RIGHT, buff=0.08).move_to([0, 1.2, 0])
        self.play(FadeIn(segs))
        win = SurroundingRectangle(VGroup(*segs[1:11]), color=C_YELLOW, buff=0.08)
        lab = T("t = 47.0 s · MEDIA-SEQUENCE 1", 22, C_YELLOW).next_to(win, DOWN, buff=0.3)
        with self.vo("At forty-seven seconds, the playlist has media sequence one, and lists segments one to ten. Each with an EXTINF duration, and a program date time: the wall clock."):
            self.play(Create(win), FadeIn(lab))
        win2 = SurroundingRectangle(VGroup(*segs[2:12]), color=C_YELLOW, buff=0.08)
        lab2 = T("t = 51.5 s · MEDIA-SEQUENCE 2", 22, C_YELLOW).next_to(win2, DOWN, buff=0.3)
        with self.vo("Four and a half seconds later: media sequence two, segments two to eleven. The window slid by one."):
            self.play(Transform(win, win2), Transform(lab, lab2))
        pts = [("Changed? wait at least one target duration before reloading", "The reload rules. If the playlist changed, wait at least one target duration before reloading."),
               ("Unchanged? wait half a target duration, then retry", "If it did not change, wait half a target duration, then try again."),
               ("Same number, different URI? 'It SHOULD halt playback.'", "And if the same sequence number now points at a different URI, the spec says the player should halt playback."),
               ("VOD = a playlist that stopped changing: #EXT-X-ENDLIST -> read once, stop polling", "Video on demand is just a playlist that stopped changing. It ends with EXT-X-ENDLIST, so the player reads it once and stops polling.")]
        self.bullets(pts, size=21, gap=0.22, shift=DOWN * 1.65)

    def ch_mpegts(self):
        self.new_slide("A segment is 188-byte packets (MPEG-TS)", "Open a segment, and it is a stream of hundred and eighty-eight byte packets. MPEG transport stream.", C_GREEN)
        hdr = box("4 B header", C_YELLOW, w=2.4, h=1.0, size=22)
        pay = box("184 B payload (video / audio / PAT-PMT)", C_GREEN, w=8.0, h=1.0, size=22)
        pkt = VGroup(hdr, pay).arrange(RIGHT, buff=0.04).move_to([0, 1.6, 0])
        with self.vo("Four bytes of header, a hundred and eighty-four bytes of payload."):
            self.play(FadeIn(pkt))
        fields = VGroup(T("sync 0x47", 20, C_RED), T("13-bit PID", 20, C_BLUE), T("continuity counter", 20, C_PURPLE)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(hdr, DOWN, buff=0.3)
        with self.vo("The header starts with a sync byte, hex forty-seven. Then a thirteen-bit packet ID, which says whose packet this is: audio, video, or tables. They share one byte stream: multiplexing. Then a continuity counter."):
            self.play(FadeIn(fields, lag_ratio=0.3))
        t = T("Fixed length + sync byte = both framing answers at once.  188 was chosen for ATM.", 22, C_YELLOW, maxw=12.4).next_to(fields, DOWN, buff=0.35).set_x(0)
        with self.vo("Fixed length plus a sync byte: both framing answers at once. And one eighty-eight was chosen for ATM."):
            self.play(FadeIn(t))
        tbl = self.table([["Rendition", "Segment", "188-B packets", "Overhead"],
                          ["720p", "1,613,416 B", "8,582", "3.3%"],
                          ["480p", "823,440 B", "4,380", "4.1%"],
                          ["360p", "452,328 B", "2,406", "5.6%"]], [2.4, 3.0, 3.0, 2.2], size=21, y=-1.6, row_h=0.55)
        self.reveal_rows(tbl, ["Seven twenty p: eight thousand five hundred eighty-two packets, three point three percent overhead.", "Four eighty p: four point one percent.",
                               "Three sixty p: five point six. The newer fragmented MP4, or CMAF, uses boxes instead: size, type, payload. T L V again."])

    def ch_segment_len(self):
        self.new_slide("How long should a segment be?", "How long should a segment be, with fifty million viewers?", C_ORANGE)
        self.bars([("2 s", 25, C_RED), ("3 s", 16.7, C_ORANGE), ("4 s  (our ffmpeg)", 12.5, C_YELLOW), ("6 s  (Apple)", 8.3, C_GREEN), ("30 s", 1.7, C_BLUE)],
                  25, y0=1.7, gap=0.8, left=-1.5, width=5.0, label_w=3.6, size=21, unit=" M req/s",
                  narrs=["Two-second segments: twenty-five million segment requests a second at peak, and a latency floor of six seconds, three segments.",
                         "Three seconds: sixteen point seven million, floor nine seconds.",
                         "Four seconds, what our ffmpeg run used: twelve and a half million, floor twelve seconds.",
                         "Six seconds, Apple's advice: eight point three million, floor eighteen seconds.",
                         "Thirty seconds: one point seven million a second, and ninety seconds behind. Too late."])
        t = T("Shorter: more requests, keyframes, round trips. Longer: more latency, slower reaction. Hybrid: -hls_init_time 1 -hls_time 4", 20, C_GREY, maxw=12.4).to_edge(DOWN, buff=0.35)
        with self.vo("Shorter means more requests, more keyframes, more round trips. Longer means more latency, and slower reaction to bandwidth changes. A hybrid uses one to two second segments at start-up, for a fast first frame."):
            self.play(FadeIn(t))
        self.new_slide("Playlist traffic is harder than segment traffic", "And the playlist is the harder traffic of the two.", C_RED)
        tbl = self.table([["", "Media playlist", "Segment"],
                          ["Size", "~230 B gzipped", "450-1,600 KB"],
                          ["Changes", "every 4 s", "never"],
                          ["Cache TTL", "<= ½ target duration", "minutes to forever"],
                          ["Stale copy", "stalls, or points at deleted files", "harmless"],
                          ["Billed by", "requests", "bytes"]], [2.8, 5.2, 4.2], size=22, y=0.6, row_h=0.8)
        self.reveal_rows(tbl, ["Tiny versus big.", "Changes every four seconds, versus never.", "A TTL of at most half a target duration, versus forever.",
                               "A stale playlist stalls the player or points at deleted files. A stale segment is harmless.", "And playlists are billed by requests, segments by bytes."])

    def ch_buffer(self):
        self.new_slide("The buffer is the stale cache", "The player's buffer is the stale cache.", C_TEAL)
        bar = Rectangle(width=8, height=0.8, color=C_GREY).move_to([0, 1.0, 0])
        fill = Rectangle(width=6, height=0.8, color=C_TEAL, fill_opacity=0.6, stroke_width=0).align_to(bar, LEFT).move_to(bar, aligned_edge=LEFT)
        lab = T("buffered seconds", 20, C_GREY).next_to(bar, UP, buff=0.15)
        with self.vo("When the network has a bad minute on a train, the buffer keeps the picture going."):
            self.play(Create(bar), FadeIn(lab))
            self.play(GrowFromEdge(fill, LEFT))
        with self.vo("It drains while downloads stall."):
            self.play(fill.animate.stretch_to_fit_width(0.4, about_edge=LEFT), run_time=2)
        pts = [("Large buffer: survives a bad minute; costs latency, and memory on low-end phones and TV sticks", "A large buffer survives a bad minute, but costs latency, and memory on low-end phones and TV sticks."),
               ("One-segment buffer: lowest latency; one slow segment -> stall", "A one-segment buffer gives the lowest latency, but one slow segment means a stall."),
               ("More bandwidth -> a smaller buffer suffices. When the playlist stops moving, the buffer keeps playing", "More bandwidth means a smaller buffer is enough. When the playlist stops moving, the buffer keeps playing.")]
        self.bullets(pts, size=21, gap=0.3, shift=DOWN * 1.4)

    def ch_latency(self):
        self.new_slide("Latency is a budget", "Latency is a budget. How far behind the stadium are you?", C_YELLOW)
        parts = [("encode", 2, C_BLUE), ("segment fills", 4, C_PURPLE), ("to CDN", 2, C_TEAL), ("hold-back 3 × 4 s", 12, C_RED)]
        nars = ["Encoding: about two seconds.", "The segment has to fill: four seconds.", "Getting it to the CDN: about two seconds.", "And the player's hold-back: three target durations, twelve seconds."]
        x = -6.0
        g = VGroup()
        for (n, s, c), nar in zip(parts, nars):
            r = Rectangle(width=s * 0.47, height=0.8, color=c, fill_opacity=0.6).move_to([x + s * 0.235, 1.2, 0])
            t = T(f"{n}\n{s} s", 16, WHITE, maxw=s * 0.47 - 0.05).move_to(r)
            with self.vo(nar):
                self.play(GrowFromEdge(r, LEFT), FadeIn(t), run_time=0.6)
            g.add(VGroup(r, t))
            x += s * 0.47
        tot = T("≈ 20 s behind", 26, C_RED).next_to(g, RIGHT, buff=0.25)
        with self.vo("About twenty seconds behind the stadium, with four-second segments."):
            self.play(FadeIn(tot))
        tbl = self.table([["LL-HLS idea", "What it is"],
                          ["Parts", "~1 s pieces of a segment (>= 3× the P95 round trip)"],
                          ["Blocking playlist reload", "?_HLS_msn=... held until it exists = long polling"],
                          ["Preload hints", "name the next part early - replaced HTTP/2 push (Jan 2020)"],
                          ["Delta updates", "EXT-X-SKIP drops old entries - diffs for playlists"]], [4.0, 8.6], size=20, y=-1.4, row_h=0.6)
        self.reveal_rows(tbl, ["Low-Latency HLS is four ideas from earlier weeks. Parts: one-second pieces of a segment.",
                               "Blocking playlist reload: the request is held until that segment exists. Long polling.",
                               "Preload hints name the next part early. They replaced HTTP two server push, in January twenty twenty.",
                               "And delta updates: EXT-X-SKIP drops old entries. Diffs, for playlists. With one-second parts and a part hold-back of three parts, you get to about three seconds."])

    def ch_spoiler(self):
        self.new_slide("The spoiler problem", "Now a problem only live sport has. The spoiler.", C_RED)
        ax = NumberLine(x_range=[0, 22, 2], length=11, color=C_GREY, include_numbers=False).shift(UP * 0.6)
        self.play(Create(ax))
        evs = [(0, "wicket!", C_YELLOW, "The wicket falls at zero seconds."),
               (10, "scorecard shows W", C_RED, "The scorecard shows it at about ten seconds."),
               (20, "video shows it", C_GREEN, "And the video shows it at about twenty.")]
        for s, l, c, n in evs:
            d = Dot(ax.n2p(s), color=c, radius=0.1)
            t = T(f"{l}\n{s} s", 20, c).next_to(d, UP, buff=0.2)
            with self.vo(n):
                self.play(FadeIn(d), FadeIn(t))
        br = BraceBetweenPoints(ax.n2p(10), ax.n2p(20), DOWN, color=C_RED)
        with self.vo("For ten seconds, the scorecard spoils the video."):
            self.play(FadeIn(br), FadeIn(T("10 s spoiler window", 22, C_RED).next_to(br, DOWN)))
        t = T("Fix: stamp each update with the ball's wall-clock time; reveal it only when playback passes that #EXT-X-PROGRAM-DATE-TIME.", 21, C_GREEN, maxw=12.4).to_edge(DOWN, buff=0.5)
        with self.vo("The fix: stamp each update with the ball's wall-clock time. The player knows each segment's program date time, so it reveals the update only when playback passes that moment."):
            self.play(FadeIn(t))

    def ch_abr(self):
        self.new_slide("ABR: who decides 'worse'?", "Adaptive bitrate. Who decides what is worse? The player, at every segment, under a policy the product sets.", C_BLUE)
        ax = Axes(x_range=[0, 12, 1], y_range=[0, 4, 1], x_length=10, y_length=3.2, axis_config={"color": C_GREY, "include_ticks": False}).shift(UP * 0.4)
        bw = ax.plot(lambda x: 2.8 + 0.9 * np.sin(x * 0.9) - (1.6 if 5 < x < 8 else 0), color=C_BLUE, use_smoothing=False)
        steps = VGroup()
        levels = [3, 3, 2, 3, 3, 2, 1, 1, 2, 3, 3, 3]
        for i, lv in enumerate(levels):
            y = {1: 0.8, 2: 1.75, 3: 3.44}[lv] * 0.75
            steps.add(Line(ax.c2p(i, y), ax.c2p(i + 1, y), color=C_YELLOW, stroke_width=6))
        self.play(Create(ax))
        with self.vo("The blue line is the throughput the network gives you. It wobbles, and then dips, maybe a tunnel."):
            self.play(Create(bw), run_time=2)
        with self.vo("The yellow steps are the rendition the player picks for each segment. It steps down before the buffer runs dry, and back up when things recover."):
            self.play(Create(steps, lag_ratio=0.5), run_time=3)
        pts = [("Throughput-based: measure recent segments, pick the highest rendition that fits - congestion control, one layer up", "Throughput-based A B R measures how fast recent segments arrived, and picks the highest rendition that fits. Congestion control, one layer up."),
               ("Buffer-based: nearly empty -> step down; full -> step up. Netflix: 10-20% fewer rebuffers (SIGCOMM 2014)", "Buffer-based A B R steps down when the buffer is nearly empty, and up when it is full. Netflix's A B tests showed ten to twenty percent fewer rebuffers."),
               ("Policy: a stall is worse than a lower rendition. Apple: start cellular at 730 kbps, Wi-Fi at 2 Mbps", "And the policy: a stall is worse than a lower rendition. Apple suggests starting cellular at seven hundred thirty kilobits, and Wi-Fi at two megabits.")]
        self.bullets(pts, size=19, gap=0.18, shift=DOWN * 2.35)

    def ch_multicdn(self):
        self.new_slide("Many origins, many CDNs", "At this scale, you use more than one CDN, and more than one origin.", C_PURPLE)
        app = box("Android app", C_YELLOW, w=2.4).move_to([-5.2, 1.3, 0])
        a = VGroup(box("CDN A edge", C_BLUE, w=2.4), box("A mid-tier", C_BLUE, w=2.4), box("Origin 1", C_ORANGE, w=2.2)).arrange(RIGHT, buff=0.5).move_to([1.4, 2.1, 0])
        b = VGroup(box("CDN B edge", C_TEAL, w=2.4), box("B mid-tier", C_TEAL, w=2.4), box("Origin 2", C_ORANGE, w=2.2)).arrange(RIGHT, buff=0.5).move_to([1.4, 0.5, 0])
        arr = VGroup(Arrow(app.get_right(), a[0].get_left(), color=C_BLUE, buff=0.1), Arrow(app.get_right(), b[0].get_left(), color=C_TEAL, buff=0.1),
                     *[Arrow(g[i].get_right(), g[i + 1].get_left(), color=C_GREY, buff=0.05) for g in (a, b) for i in range(2)])
        with self.vo("The app talks to CDN A as primary: edge, mid-tier, origin one with its own packager. CDN B is the fallback, with origin two. Same segment names on both."):
            self.play(FadeIn(app), FadeIn(a), FadeIn(b), Create(arr), run_time=1.5)
        tbl = self.table([["Mechanism", "How", "Trade"],
                          ["DNS", "a CDN per region / ISP", "slow: resolvers cache"],
                          ["Listed twice", "master lists each rendition per CDN", "stream failover"],
                          ["Content Steering", "a polled JSON names the preferred CDN", "standardised re-polling"],
                          ["Client failover", "errors trip a circuit breaker; next segment tries the other", "Session 7"]],
                         [3.0, 6.0, 3.6], size=19, y=-1.9, row_h=0.42)
        self.reveal_rows(tbl, ["How to choose. DNS hands out a CDN per region, but resolvers cache, so it is slow to change.", "List each rendition twice in the master, once per CDN.",
                               "Content Steering: a JSON file, polled every TTL, names the preferred CDN.", "Or client failover: errors on one CDN trip a circuit breaker, and the next segment tries the other. Session seven."])

    def ch_stale_404(self):
        self.new_slide("Stale playlists and deleted segments", "Serve stale is your friend. With one catch, for live video.", C_RED)
        _, bx = self.flow(["ffmpeg deletes\nseg_000000\n4 s after it leaves", "origin blip:\nCDN serves a\nstale playlist", "stale playlist lists\na deleted segment", "404, negatively\ncached ->\nplayer stalls"],
                          [C_ORANGE, C_YELLOW, C_PURPLE, C_RED], y=1.0, w=2.9, h=1.6, size=19, gap=0.35,
                          narrations=["ffmpeg's delete segments option keeps only one unreferenced segment. Segment zero vanished four seconds after it left the playlist.",
                                      "Then the origin blips, and the CDN, correctly, serves a stale playlist.",
                                      "But the stale playlist lists a segment the origin already deleted.",
                                      "Four oh four. Negatively cached. The player stalls. Serve stale may cause player issues."])
        pts = [("RFC 8216: a removed segment MUST stay available for its duration + the playlist's duration: 4 + 40 = 44 s", "The R F C says a removed segment must stay available for its own duration plus the playlist's. Four plus forty: forty-four seconds."),
               ("Fixes: -hls_delete_threshold 12; playlist TTL <= ½ target duration; serve stale playlists for one target duration at most", "Fixes: raise the delete threshold. Keep the playlist TTL at most half a target duration, and serve a stale playlist for one target duration at most. Segments never change, so serve those stale freely."),
               ("Apple: a playlist is invalid when Last-Modified is > 3 target durations behind Date", "Apple adds: treat a playlist as invalid when its Last-Modified is more than three target durations behind the Date.")]
        self.bullets(pts, size=20, gap=0.25, shift=DOWN * 1.7)
        self.new_slide("Caching rules for a live stream", "Putting it together: caching rules for a live stream.", C_GREEN)
        tbl = self.table([["Object", "TTL", "Serve stale", "404 TTL"],
                          ["master.m3u8", "minutes", "yes", "1 s"],
                          ["media playlist", "<= ½ target dur.", "1 target dur. max", "1 s or none"],
                          ["segment .ts", "long (never changes)", "yes", "<= 1 s at live edge"],
                          ["score.json", "<= ½ your promise", "while updating", "1 s (5xx 2 s)"]], [3.2, 3.6, 3.2, 3.0], size=21, y=1.0, row_h=0.75)
        self.reveal_rows(tbl, ["The master: minutes.", "The media playlist: at most half a target duration, stale for one at most.", "Segments: long, they never change.", "And the scorecard: at most half your freshness promise."])
        t = T("Also: gzip every playlist (Apple: MUST) · keep per-viewer tokens out of the cache key", 22, C_YELLOW, maxw=12.4).to_edge(DOWN, buff=0.6)
        with self.vo("Also, gzip every playlist. Apple says must. And keep per-viewer tokens out of the cache key, or every viewer gets their own copy."):
            self.play(FadeIn(t))

    def ch_ffmpeg(self):
        self.new_slide("Making the stream with ffmpeg", "Finally, making the stream yourself, with ffmpeg.", C_ORANGE)
        code = self.code_block(["ffmpeg -re -i input.mp4 -codec: copy -hls_time 4 -hls_list_size 5 \\",
                                "       -hls_playlist_type event -f hls index.m3u8"], size=20, pos=UP * 1.9, hl={"-re": C_YELLOW, "-codec: copy": C_RED, "-hls_time 4": C_GREEN})
        with self.vo("A one-liner. Dash r e reads at native speed: a file pretending to be a camera. Codec copy means no re-encode. Hls time four asks for four-second segments."):
            self.play(FadeIn(code))
        t = T("Result: 8.33 s segments, not 4.  x264's default keyframe interval = 250 frames = 8.33 s at 30 fps.", 22, C_RED, maxw=12.4).shift(UP * 0.6)
        with self.vo("What actually came out: eight point three three second segments. Because with codec copy, ffmpeg can only cut at existing keyframes, and x264's default keyframe interval is two hundred fifty frames. Hls time is a target, not a promise."):
            self.play(FadeIn(t))
        _, bx = self.flow(["camera", "RTMP / SRT", "transcoder", "packager", "origin", "CDN"], [C_BLUE, C_PURPLE, C_ORANGE, C_YELLOW, C_GREEN, C_TEAL], y=-0.6, w=1.8, h=0.7, size=18, gap=0.35,
                          narrations=["A real pipeline: camera,", "ingest over RTMP or SRT,", "transcoder,", "packager,", "origin,", "and CDN."])
        pts = [("ABR ladder: split=3 - decode once, encode three times (720p 3000k, 480p 1500k, 360p 800k)", "The A B R ladder: split equals three. Decode once, encode three times: seven twenty p at three thousand k, four eighty at fifteen hundred, three sixty at eight hundred."),
               ("-g 120 -keyint_min 120 -sc_threshold 0: a keyframe every 120 frames = 4 s at 30 fps only (24 fps gave 5 s)", "A keyframe every hundred twenty frames, with scene-cut keyframes disabled. That is four seconds, but only at thirty frames per second. A twenty-four fps source gave five-second segments."),
               ("-hls_flags independent_segments+delete_segments+omit_endlist+program_date_time: a 40 s window that never ends, stamped with wall-clock time", "And the flags give a forty-second window that never ends, stamped with wall-clock time.")]
        self.bullets(pts, size=19, gap=0.2, shift=DOWN * 2.45)

    def ch_course(self):
        self.new_slide("The whole course in one cricket match", "And that is the whole course, in one cricket match.", C_YELLOW)
        tbl = self.table([["Week", "Shows up as"],
                          ["1 Sockets", "16-bit ports -> 28k test sockets per IP; base64 in the WebSocket handshake"],
                          ["2 Wire", "framing: SSE blank line, WebSocket lengths, 188-B packets; control vs data"],
                          ["3 Scale", "50 M held sockets, Little's Law, nothing free per connection"],
                          ["4 nginx", "proxy_cache_lock, use_stale, one location per file type"],
                          ["5 HTTP", "ETag & 304, keep-alive, 101 Upgrade, push's death shaping LL-HLS"],
                          ["6 CDNs", "tiers, collapsing, negative caching, per request vs per byte"],
                          ["7 Failures", "jitter, the live-edge 404, stale-if-error, failover, who decides 'worse'"],
                          ["8 Video", "HLS: a playlist polled like a scorecard, pointing at bytes that never change"]],
                         [2.4, 10.4], size=19, y=0.0, row_h=0.7)
        self.reveal_rows(tbl, ["Week one, sockets: sixteen-bit ports, and base sixty-four in the WebSocket handshake.", "Week two, the wire: framing everywhere. Blank lines, lengths, fixed packets.",
                               "Week three, scale: fifty million held sockets, and Little's Law.", "Week four, nginx: cache lock, use stale.",
                               "Week five, HTTP: ETags, three oh fours, the one oh one upgrade, and push's death shaping LL-HLS.", "Week six, CDNs: tiers, collapsing, negative caching, and which bill you are on.",
                               "Week seven, failures: jitter, the live-edge four oh four, stale if error, failover.", "And week eight: H L S, a playlist polled like a scorecard, pointing at bytes that never change."])

    def ch_four_ideas(self):
        self.new_slide("Four ideas to keep", "Four ideas to keep.", C_GREEN)
        pts = [("Pull scales through caches; push scales through machines. Same answer for everyone -> CDN. Different per person -> you're buying sockets", "One. Pull scales through caches. Push scales through machines. If the answer is the same for everyone, use a CDN. If it is different per person, you are buying sockets."),
               ("Number the pieces, then cache them forever: a small changing index + immutable numbered pieces", "Two. Number the pieces, then cache them forever. A small changing index, plus immutable numbered pieces."),
               ("Latency is a budget you spend on safety: poll intervals, TTLs, segment length, hold-back all add up", "Three. Latency is a budget you spend on safety. Poll intervals, TTLs, segment length and hold-back all add up."),
               ("Know which bill you're on: below ~11 KB per request, above it per byte", "And four. Know which bill you are on. Below about eleven kilobytes you pay per request. Above it, per byte.")]
        self.bullets(pts, size=24, gap=0.45, colors=[C_GREEN, C_BLUE, C_YELLOW, C_ORANGE])

    def quiz(self):
        self.quiz_recap(8, [
            "50 M peak, 20 M avg, 4-hour match; scorecard ~1 KB gzipped; 100 events a year.",
            "Polling (stateless, cacheable) vs persistent: long poll, SSE, WebSocket, MQTT, raw socket (stateful, not cacheable).",
            "Jitter +/-20%. Staleness = poll interval + sum of TTLs; CDN TTL <= ½ promise; prefresh. Long poll ~25 s, beat 60 s idle timeouts.",
            "SSE: text/event-stream, blank-line delimiter, Last-Event-ID, retry:. WebSocket: 101, Accept = base64(SHA-1(key + GUID)), 126/127 lengths, client frames masked.",
            "MQTT: retained message, QoS 1 at-least-once, PINGREQ C0 00, varint length. Hotstar + EMQX: 250k/node, 4 M per ELB, 50 M on 200 nodes (2019).",
            "Little's Law: polling 50k in flight vs push 50 M sockets. 9.6 B requests, 1.67 M req/s, 9.6 TB per match. S3 5,500 GET/s per prefix -> 503 Slow Down.",
            "CDN: 92% request fees for 1 KB; break-even ~11 KB. Push cheapest, CDN dearest. 304 saves bytes, not the request fee.",
            "Negative caching: 5xx 1-2 s; 404 ~never (Cloudflare default 3 min). JSON Patch 183 B vs 1,088 B.",
            "HLS: master (once) -> media playlist (every target duration) -> segments (once). MEDIA-SEQUENCE, TARGETDURATION, EXTINF, PROGRAM-DATE-TIME, ENDLIST.",
            "BANDWIDTH = (v + a) × 1.1. Reload: changed -> >= 1 target duration; unchanged -> ½.",
            "MPEG-TS: 188-byte packets, sync 0x47, 13-bit PID, 4-byte header, chosen for ATM. fMP4/CMAF = boxes.",
            "Segment length trade-off; Apple 6 s; latency floor 3× segment; ~20 s with 4 s segments. LL-HLS: parts, blocking reload, preload hints, EXT-X-SKIP -> ~3 s.",
            "Spoiler fix: wall-clock stamp + PROGRAM-DATE-TIME. ABR: throughput vs buffer-based; a stall is worse than lower quality.",
            "Multi-CDN: DNS, listed twice, Content Steering, client failover. Removed segment stays 44 s; Apple: invalid if Last-Modified > 3 target durations old.",
            "ffmpeg: -codec copy cuts at keyframes; x264 default GOP 250 -> 8.33 s; -g 120 = 4 s @ 30 fps; split=3 decode once, encode thrice.",
        ], "Here is what the quiz is most likely to ask from session eight.", size=23, per_page=3)
        self.clear()
        end = VGroup(T("Every live stream is a scorecard with bigger bytes.", 34, C_YELLOW, font=SERIF), T("Computer Networks · Sessions 1-8", 24, C_GREY)).arrange(DOWN, buff=0.5)
        with self.vo("That is session eight, and the end of the course. From one echo server and seven system calls, to one cricket match on fifty million phones. Every live stream is a scorecard with bigger bytes. Good luck in the quiz."):
            self.play(FadeIn(end, shift=UP * 0.2), run_time=1.2)
        self.wait(1.5)
