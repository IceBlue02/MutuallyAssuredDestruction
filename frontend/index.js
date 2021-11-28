const P1 = 1,
    P2 = -1;
const TILE_RED = 1,
    TILE_GREY = 0,
    TILE_BLUE = -1;
const BUILDING_EMPTY = 0,
    BUILDING_FACTORY = 1,
    BUILDING_SILO = 2;
const BOMB_SQUARE = 1,
    BOMB_CIRCLE = 2,
    BOMB_DIAMOND = 3,
    BOMB_TARGET = 4,
    BOMB_DOT_DOT_DOT = 5,
    BOMB_X = 6,
    BOMB_H_BOMB = 7,
    BOMB_P_BOMB = 8,
    BOMB_CHERRY = 9,
    BOMB_E = 10,
    BOMB_A_BOMB = 11,
    BOMB_ENGLAND = 12;

const RED = "#fe2b2b";
const BLUE = "#3f14ff";

const state = {
    mouse: {
        x: 0,
        y: 0,
        down: false,
    },
    animation: 0,
    cursorPointer: false,
    wasClickThisFrame: false,
    /** @type {HTMLCanvasElement} */
    canvas: null,
    /** @type {CanvasRenderingContext2D} */
    ctx: null,
};

const HOST = "http://127.0.0.1:5000";

const delay = async (miliseconds) => {
    return new Promise((resolve) => setTimeout(() => resolve(), miliseconds));
};

const post = async (endpoint, body = null) => {
    return await fetch(`${HOST}/${endpoint}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    }).then((x) => x.json());
};

const get = async (endpoint) => {
    return await fetch(`${HOST}/${endpoint}`, { method: "GET" }).then((x) => x.json());
};

const asset = (src) => {
    const img = new Image();
    img.src = "assets/" + src;
    return img;
};
const rect = (x, y, w, h) => ({ x, y, w, h });

const getViewport = () => {
    const { width, height } = state.canvas;
    const scale = Math.min(width / 1920, height / 1080);
    return {
        xo: (width - 1920 * scale) / 2,
        yo: (height - 1080 * scale) / 2,
        scale,
    };
};

const drawRect = ({ x, y, w, h }, colour) => {
    if (colour) state.ctx.fillStyle = colour;
    const { xo, yo, scale } = getViewport();
    state.ctx.fillRect(x * scale + xo, y * scale + yo, w * scale, h * scale);
};
const drawImage = ({ x, y, w, h }, image, rotation, imageScale) => {
    state.ctx.save();
    const { xo, yo, scale } = getViewport();
    x = x * scale + xo;
    y = y * scale + yo;
    w *= scale;
    h *= scale;
    if (rotation || imageScale) {
        state.ctx.translate(x + w / 2, y + h / 2);
        if (imageScale) state.ctx.scale(imageScale, imageScale);
        state.ctx.rotate((rotation * Math.PI) / 180.0);
        state.ctx.translate(-x - w / 2, -y - h / 2);
    }
    state.ctx.drawImage(image, x, y, w, h);
    state.ctx.restore();
};
const drawText = (x, y, text, size, colour, outline, outlineSize = 2) => {
    const { xo, yo, scale } = getViewport();
    state.ctx.font = `${size * scale}px sans-serif`;
    state.ctx.fillStyle = colour;
    const { width } = state.ctx.measureText(text);

    const rx = x * scale + xo - width / 2;
    const ry = y * scale + yo + size / 2;
    if (outline) {
        state.ctx.strokeStyle = outline;
        state.ctx.lineWidth = outlineSize * scale;
        state.ctx.strokeText(text, rx, ry);
    }

    state.ctx.fillText(text, rx, ry);
};
const collideRect = ({ x, y }, { x: rx, y: ry, w: rw, h: rh }) => {
    if (x < rx || y < ry || x >= rx + rw || y >= ry + rh) return false;
    return true;
};

const tween = (speed = 1) => Math.sin(speed * 2 * Math.PI * state.animation);
const step = (from, to, decay = 3) => (typeof from === "undefined" ? to : from + (to - from) / decay);

class Entity {
    constructor(rect) {
        this._scale = 1;
        this._rotation = 0;
        this.rect = rect;
        this._rect = { ...rect };
        this.animateScale = false;
        this.animateRotataion = false;
        this.animatePos = false;
        this.stepSpeed = 3;
    }
    setRect(rect) {
        this.rect = { ...rect };
        if (!this.animatePos) this._rect = { ...rect };
    }
    render() {
        if (this.animatePos) {
            this._rect.x = step(this._rect.x, this.rect.x, this.stepSpeed);
            this._rect.y = step(this._rect.y, this.rect.y, this.stepSpeed);
            this._rect.w = step(this._rect.w, this.rect.w, this.stepSpeed);
            this._rect.h = step(this._rect.h, this.rect.h, this.stepSpeed);
        } else this._rect = this.rect;
        this._render();
    }
    _render() {}
}
class ImageEntity extends Entity {
    constructor(rect) {
        super(rect);
        this.image = null;
        this.scale = 1;
        this.rotation = 0;
    }
    setScale(scale) {
        this.scale = scale;
        if (!this.animateScale) this._scale = this.scale;
    }
    setRotation(rotation) {
        this.rotation = rotation;
        if (!this.animateRotataion) this._rotation = this.rotation;
    }
    _render() {
        this._rotation = step(this._rotation, this.rotation);
        this._scale = step(this._scale, this.scale);
        if (this.image) drawImage(this._rect, this.image, this._rotation, this._scale);
    }
}

class RectEntity extends Entity {
    constructor(rect, colour) {
        super(rect);
        this.colour = colour;
    }
    _render() {
        drawRect(this._rect, this.colour);
    }
}

const tileImage = (type) => (type === TILE_RED ? redTile : type === TILE_BLUE ? blueTile : greyTile);
class Tile extends ImageEntity {
    constructor(rect, type) {
        super(rect);
        this.animateScale = true;
        this.type = type;
        this.image = tileImage(type);
    }
}

class Card extends ImageEntity {
    constructor(game, rect, bombId, showFace = true) {
        super(rect);
        this.bombId = bombId;
        this.image = showFace ? game.cards[bombId].image : cardBackRed;
        this.animatePos = true;
        this.animateScale = true;
    }
}

class Hand {
    constructor(game, player) {
        this.game = game;
        this.cards = [];

        this.player = player;
        this.large = this.player === P1;

        this.selectedCard = null;
    }
    addCard(type, showFace = true) {
        this.cards.push(new Card(this.game, rect(), type, showFace));
    }
    render() {
        const cardWidth = this.large ? (this.game.selectionActive ? 200 : 150) : 100;
        const cardHeight = cardWidth * 1.4;

        const isP1 = this.player === P1;

        const cardOverlap = cardWidth / ((this.cards.length + 5) / this.cards.length);
        const hoverXOffset = cardOverlap / 2;
        const hoverYOffset = cardWidth * 0.2;
        const selectedYOffset = cardWidth / 2;

        let x = isP1 ? 75 : 1920 - 75 - cardWidth;
        let y = 1080 - cardHeight - 25;
        let hoverCard = null,
            selectedCard = null,
            newSelectedCard = null;
        this.cards.forEach((card, n) => {
            const topCard = !isP1 ? n === 0 : n === this.cards.length - 1;
            const bottomCard = isP1 ? n === 0 : n === this.cards.length - 1;

            const hover =
                isP1 &&
                collideRect(
                    state.mouse,
                    rect(
                        x + !isP1 * hoverXOffset * !bottomCard,
                        y - hoverYOffset,
                        cardWidth - (topCard ? 0 : hoverXOffset),
                        cardHeight + hoverYOffset
                    )
                );
            const selected = this.game.selectionActive && isP1 && card === this.game.selectedCard;

            card.rect = rect(x, y, cardWidth, cardHeight);

            if (selected) {
                card.rect.y -= selectedYOffset;
                selectedCard = card;
            } else if (hover) {
                card.rect.y -= hoverYOffset;
                hoverCard = card;
            } else {
                card.render();
            }

            if (hover && this.game.selectionActive) state.cursorPointer = true;

            card.setRotation(0);
            card.setScale(1);
            if (hover) {
                card.setRotation(tween(2) * 1.5);
                card.setScale(1.05);
            }
            if (selected) {
                card.setRotation(tween(0.5) * 2);
                card.setScale(1.1);
            }

            const step = cardWidth - cardOverlap + (hover || selected ? hoverXOffset : 0);
            if (isP1) x += step;
            else x -= step;

            if (this.game.selectionActive && state.wasClickThisFrame && isP1 && hover) newSelectedCard = card;
        });

        if (newSelectedCard !== null) {
            if (newSelectedCard === this.game.selectedCard) this.game.selectCard(null);
            else this.game.selectCard(newSelectedCard);
        }
        if (selectedCard) selectedCard.render();
        if (hoverCard) hoverCard.render();
    }
}

class CardSelector {
    constructor(game) {
        this.game = game;
        this.cards = [];

        this.active = false;
    }

    newSelection(choices) {
        this.cards = [];
        choices.forEach((x) => this.addCard(x));
    }

    addCard(type) {
        const card = new Card(this.game, rect(), type);
        this.cards.push(card);
        card.animateScale = false;
        card.setScale(0);
        card.animateScale = true;
    }

    render() {
        if (!this.active) return;

        const cardWidth = this.cards.length > 5 ? 150 : 200;
        const cardHeight = cardWidth * 1.4;
        const cardGap = cardWidth * 0.1;

        const width = this.cards.length * cardWidth + (this.cards.length - 1) * cardGap;
        let x = (1920 - width) / 2;
        let y = (1080 - cardHeight) / 2 - 50;

        for (const card of this.cards) {
            card.rect = rect(x, y, cardWidth, cardHeight);
            const hover = collideRect(state.mouse, card.rect);
            if (hover && state.wasClickThisFrame) this.game.chooseNewCard(card);
            card.render();
            card.setScale(hover ? 1.1 : 1);
            card.setRotation(hover ? tween(2) * 2 : 0);
            if (hover) state.cursorPointer = true;
            x += cardWidth + cardGap;
        }

        drawText(960, 685, "Select one card", 54 + tween(0.75) * 10, "#fff", RED, 0);
    }
}

class NoCardsBanner {
    QUIPS = [
        "Should have placed those silos better",
        "Better luck next time. If there's a next time.",
        "No hard feelings, but that's not cool",
        "Seriously, already?",
    ];
    FACTORY_QUIPS = [
        "Should have placed those factories better",
        "Guess you're on your last leg now",
        "A bomber without factories is a dead bomber - you, just now",
    ];

    constructor(game) {
        this.game = game;
        this.banner = new RectEntity(rect(), RED);

        this.showing = this.hiding = false;
        this.alpha = 0;
        this.showTime = this.hideTime = null;
        this.quip = "";
    }
    show() {
        const quips = this.game.grid.entities.find(
            ([[x, y], entity]) => entity instanceof Factory && this.game.grid.tiles[x][y].type === this.game.player
        )
            ? this.QUIPS
            : this.FACTORY_QUIPS;
        this.quip = quips[Math.floor(Math.random() * quips.length)];

        const height = 1080 / 3;
        this.showing = true;
        this.showTime = state.animation;

        this.showTime = state.animation;
        this.banner.rect = rect(0, 540 - height / 2, 0, height);
        this.banner._rect = { ...this.banner.rect };
        this.banner.animatePos = true;
        this.banner.rect.w = 1920;
        this.banner.stepSpeed = 15;

        delay(4000).then(() => this.hide());
    }
    hide() {
        this.hideTime = state.animation;
        this.showing = false;
        this.hiding = true;
        this.banner.stepSpeed = 10;

        this.banner.rect.x = 1920;
        this.banner.rect.w = 0;

        this.hideTime = state.animation;
    }
    render() {
        this.banner.colour = this.game.player === P1 ? RED : BLUE;
        this.banner.render();

        if (this.showing) this.alpha = Math.min(1, (state.animation - this.showTime) * 3);
        else if (this.hiding) this.alpha = 1 - Math.min(1, (state.animation - this.hideTime) * 3);

        drawText(1920 / 2, 1080 / 2 - 50, "No cards this turn", 100, `rgba(255, 255, 255, ${this.alpha})`);
        drawText(1920 / 2, 1080 / 2 + 50, `${this.quip}`, 42, `rgba(255, 255, 255, ${this.alpha})`);
    }
}

class Grid {
    WIDTH = 30;
    HEIGHT = 15;

    RECT = rect(300, 50, 1920 - 600, 1080 - 400);

    TILE_WIDTH = this.RECT.w / this.WIDTH;
    TILE_HEIGHT = this.RECT.h / this.HEIGHT;

    constructor(game) {
        this.game = game;
        this.tiles = [];
        for (let x = 0; x < this.WIDTH; x++) {
            this.tiles.push([]);
            for (let y = 0; y < this.HEIGHT; y++) {
                this.tiles[x].push(
                    new Tile(
                        rect(
                            this.RECT.x + x * this.TILE_WIDTH,
                            this.RECT.y + y * this.TILE_HEIGHT,
                            this.TILE_WIDTH,
                            this.TILE_HEIGHT
                        ),
                        TILE_GREY
                    )
                );
            }
        }
        this.entities = [];
    }

    setTile(x, y, type) {
        this.tiles[x][y].type = type;
        this.tiles[x][y].image = tileImage(type);
    }

    render() {
        let hoverTile = null;
        this.tiles.forEach((col, x) => {
            col.forEach((tile, y) => {
                tile.render();
                const hover =
                    collideRect(state.mouse, tile.rect) &&
                    (this.game.selectedCard ||
                        ((this.game.factoryPlacer.active || this.game.siloPlacer.active) &&
                            tile.type === this.game.player));
                if (hover) hoverTile = [x, y];
                tile.setScale(1);

                if (hover && this.game.selectedCard && state.wasClickThisFrame) this.game.playCard(x, y);
                if (hover && this.game.factoryPlacer.active && state.wasClickThisFrame) this.game.placeFactory(x, y);
                if (hover && this.game.siloPlacer.active && state.wasClickThisFrame) this.game.placeSilo(x, y);
            });
        });

        const hovers = [];
        if (hoverTile && this.game.selectedCard !== null) {
            for (let dx = 0; dx < 5; dx++) {
                for (let dy = 0; dy < 5; dy++) {
                    if (this.game.selectedBombShape[dy][dx]) {
                        hovers.push([hoverTile[0] + dx - 2, hoverTile[1] + dy - 2]);
                    }
                }
            }
        }
        if (hoverTile && (this.game.factoryPlacer.active || this.game.siloPlacer.active)) hovers.push(hoverTile);

        for (const [[x, y], entity] of this.entities) {
            entity.rect.x = this.RECT.x + x * this.TILE_WIDTH;
            entity.rect.y = this.RECT.y + y * this.TILE_HEIGHT;
            entity.rect.w = this.TILE_WIDTH;
            entity.rect.h = this.TILE_HEIGHT;
            entity.render();
            entity.setScale(1);
        }

        for (const [x, y] of hovers) {
            state.cursorPointer = true;
            this.tiles[x]?.[y]?.setScale(0.5);
            for (const e of this.entities) {
                if (e[0][0] === x && e[0][1] === y) e[1].setScale(0.5);
            }
        }
    }
}

class TurnIndicator {
    constructor(game) {
        this.game = game;
        this.top = new RectEntity(rect(), RED);
        this.bottom = new RectEntity(rect(), RED);

        this.showing = this.hiding = false;
        this.alpha = 0;
        this.showTime = this.hideTime = null;
    }
    render() {
        const redTurn = this.game.playerTurn === P1;
        this.top.colour = redTurn ? RED : BLUE;
        this.bottom.colour = redTurn ? RED : BLUE;

        const text = this.game.playerTurn === this.game.player ? "Your" : redTurn ? "Red's" : "Blue's";

        this.top.render();
        this.bottom.render();

        if (this.showing) this.alpha = Math.min(1, (state.animation - this.showTime) * 3);
        else if (this.hiding) this.alpha = 1 - Math.min(1, (state.animation - this.hideTime) * 3);

        drawText(1920 / 2, 1080 / 2 - 75, `Turn ${this.game.turn}`, 200, `rgba(255, 255, 255, ${this.alpha})`);
        drawText(1920 / 2, 1080 / 2 + 75, `${text} turn`, 100, `rgba(255, 255, 255, ${this.alpha})`);
    }
    show() {
        const height = 1080 / 4;
        this.showing = true;

        this.showTime = state.animation;
        this.top.rect = rect(0, 540 - height, 0, height);
        this.top._rect = { ...this.top.rect };
        this.top.animatePos = true;
        this.bottom.rect = rect(1920, 540, 0, height);
        this.bottom._rect = { ...this.bottom.rect };
        this.bottom.animatePos = true;
        this.top.stepSpeed = 15;
        this.bottom.stepSpeed = 15;

        this.top.rect.w = 1920;
        this.bottom.rect.x = 0;
        this.bottom.rect.w = 1920;
        delay(2500).then(() => this.hide());
    }
    hide() {
        this.showing = false;
        this.hiding = true;
        this.top.stepSpeed = 10;
        this.bottom.stepSpeed = 10;
        this.top.rect.x = 1920;
        this.top.rect.w = 0;
        this.bottom.rect.w = 0;

        this.hideTime = state.animation;
    }
}

class Factory extends ImageEntity {
    constructor(rect) {
        super(rect);
        this.image = asset("factory.png");
        this.animateScale = true;
    }
}

class Silo extends ImageEntity {
    constructor(rect) {
        super(rect);
        this.image = asset("silo.png");
        this.animateScale = true;
    }
}

class FactoryPlacer {
    constructor(game, num = 5) {
        this.game = game;
        this.left = num;
        this.active = false;
        this.factories = [];
    }

    place(x, y) {
        if (this.factories.some(([x1, y1]) => x1 === x && y1 === y)) return;
        this.factories.push([x, y]);
        this.left--;
        this.game.grid.entities.push([[x, y], new Factory(rect())]);
    }

    render() {
        if (!this.active) return;
        const plural = this.left === 1 ? "factory" : "factories";
        drawText(960, 775, `${this.left} ${plural} left to place`, 54, "#fff", RED, 0);
    }
}
class SiloPlacer {
    constructor(game, num = 5) {
        this.game = game;
        this.left = num;
        this.active = false;
        this.silos = [];
    }

    place(x, y) {
        if (this.silos.some(([x1, y1]) => x1 === x && y1 === y)) return;
        if (this.game.factoryPlacer.factories.some(([x1, y1]) => x1 === x && y1 === y)) return;
        this.silos.push([x, y]);
        this.left--;
        this.game.grid.entities.push([[x, y], new Silo(rect())]);
    }

    render() {
        if (!this.active) return;
        const plural = this.left === 1 ? "silo" : "silos";
        drawText(960, 775, `${this.left} ${plural} left to place`, 54, "#fff", RED, 0);
    }
}

class Game {
    constructor() {
        this.cards = {};

        this.turn = 0;
        this.playerTurn = P1;

        this.selectedBombShape = null;
        this.selectionActive = false;

        this.selectedCard = null;
        this.animatingCard = null;

        state.canvas = document.getElementById("root");
        /** @type {CanvasRenderingContext2D} */
        state.ctx = state.canvas.getContext("2d");

        this.startTime = Date.now();
        this.lastFrame = this.startTime;
        this.dt = 0;
        this.setupListeners();
    }

    async updateBoardAndHands(doHand = true) {
        const { board, hand, otherHand, lastPlayed } = await post("get_game_state", { player: this.player });

        const updateBoard = () => {
            this.grid.entities = [];
            board.forEach((row, x) => {
                row.forEach(([player, building], y) => {
                    this.grid.setTile(x, y, player);
                    switch (building) {
                        case BUILDING_EMPTY:
                            break;
                        case BUILDING_SILO:
                            this.grid.entities.push([[x, y], new Silo(rect())]);
                            break;
                        case BUILDING_FACTORY:
                            this.grid.entities.push([[x, y], new Factory(rect())]);
                            break;
                    }
                });
            });
        };

        let played;
        if (this.playerTurn === this.player && lastPlayed) {
            played = this.p2hand.cards[this.p2hand.cards.length - 1];
            played.bombId = lastPlayed;
        } else if (this.playedCard) played = this.playedCard;

        this.p2hand.cards = [];
        new Array(otherHand).fill(null).map(() => this.p2hand.addCard(-1, false));

        if (doHand) {
            this.p1hand.cards = [];
            hand.map((x) => this.p1hand.addCard(x));
        }

        if (played) {
            await this.flipCard(played, this.playerTurn === this.player);
            updateBoard();
        } else updateBoard();
    }
    async flipCard(played, spin) {
        this.animatingCard = played;
        played.stepSpeed = 7;

        played.setRect(rect((1920 - 250) / 2, (1080 - 350) / 2, 250, 350));

        if (spin) {
            await delay(500);
            played.rect.x = 1920 / 2;
            played.rect.w = 0;
            await delay(500);
            played.image = this.cards[played.bombId].image;
            played.rect.x = (1920 - 250) / 2;
            played.rect.w = 250;
            played.stepSpeed = 5;
            await delay(500);
        }
        await delay(1500);
        this.animatingCard = null;
    }

    async initialSetup() {
        const cards = await get("get_cards");
        for (const card of cards) {
            this.cards[card.id] = { ...card, image: asset(`cards/${card.id}.png`) };
        }

        const { player, ready } = await post("connect");
        this.player = player;

        await this.updateBoardAndHands();

        if (ready) this.startGame();
        else {
            const listener = new EventSource(`${HOST}/await_start`);
            listener.onmessage = () => {
                listener.close();
                this.startGame();
            };
        }

        const turnListener = new EventSource(`${HOST}/await_turn`);
        let resolve;
        this.turnProm = new Promise((res) => {
            resolve = res;
        });
        turnListener.onmessage = async (e) => {
            const { player } = JSON.parse(e.data);
            this.playerTurn = player;
            if (player === P1) {
                this.turn++;
            }
            await this.updateBoardAndHands();
            if (this.turn !== 1 || this.playerTurn !== P1) {
                this.turnIndicator.show();
                await delay(4000);

                resolve(player);
                this.turnProm = new Promise((res) => {
                    resolve = res;
                });
            } else {
                resolve(player);
                this.turnProm = new Promise((res) => {
                    resolve = res;
                });
            }
        };
    }
    startGame() {
        this.factoryPlacer.active = true;
    }
    beginActualGame() {
        this.turnIndicator.show();
        delay(4000).then(async () => {
            if (this.playerTurn !== this.player) while ((await this.turnProm) !== this.player);
            this.newHand();
        });
    }

    setupListeners() {
        document.addEventListener("mousemove", (e) => {
            const { xo, yo, scale } = getViewport();
            state.mouse.x = (e.clientX - xo) / scale;
            state.mouse.y = (e.clientY - yo) / scale;
        });
        document.addEventListener("mousedown", (e) => {
            if (e.button === 0) {
                state.mouse.down = true;
                state.wasClickThisFrame = true;
            }
        });
        document.addEventListener("mouseup", (e) => {
            if (e.button === 0) state.mouse.down = false;
        });

        const ro = new ResizeObserver(() => {
            const { width, height } = state.canvas.getBoundingClientRect();
            state.canvas.width = width;
            state.canvas.height = height;
        });
        ro.observe(state.canvas);
    }

    async placeFactory(x, y) {
        this.factoryPlacer.place(x, y);
        if (this.factoryPlacer.left === 0) {
            this.factoryPlacer.active = false;
            this.siloPlacer.active = true;
        }
    }
    async placeSilo(x, y) {
        this.siloPlacer.place(x, y);
        if (this.siloPlacer.left === 0) {
            this.siloPlacer.active = false;

            await post("place_starting_board", {
                player: this.player,
                factories: this.factoryPlacer.factories,
                silos: this.siloPlacer.silos,
            });

            await this.turnProm;
            this.beginActualGame();
        }
    }

    async playCard(x, y) {
        if (!this.selectedCard) return;
        state.wasClickThisFrame = false;
        const { outcome } = await post("place_bomb", {
            player: this.player,
            coords: [x, y],
            bombId: this.selectedCard.bombId,
        });
        if (!outcome) return;
        this.p1hand.cards = this.p1hand.cards.filter((x) => x !== this.selectedCard);
        this.playedCard = this.selectedCard;
        this.selectedCard = null;
        this.selectionActive = false;
        await this.updateBoardAndHands(false);

        while ((await this.turnProm) !== this.player);
        this.newHand();
    }

    async newHand() {
        const handOptions = await post("get_hand_options", { player: this.player });
        if (handOptions && handOptions.length !== 0) {
            this.cardSelector.newSelection(handOptions);
            this.cardSelector.active = true;
        } else {
            this.noCardsBanner.show();
            await delay(4000);
            this.selectionActive = true;
        }
    }

    async chooseNewCard(card) {
        state.wasClickThisFrame = false;

        const { outcome } = await post("choose_card", {
            player: this.player,
            cardId: card.bombId,
        });
        if (!outcome) return;

        this.p1hand.cards.push(card);
        this.cardSelector.active = false;
        this.selectedCard = null;
        this.selectionActive = true;
    }

    selectCard(card) {
        this.selectedCard = card;
        if (card) this.selectedBombShape = this.cards[card.bombId].shape;
    }

    updateTiming() {
        // Timing code
        const now = Date.now();
        state.animation = (now - this.startTime) / 1000;
        this.dt = (now - this.lastFrame) / 1000;
        this.lastFrame = now;
    }

    render() {
        this.updateTiming();

        const renderStats = (side) => {
            const paneRect = rect(side ? 1920 - 250 : 50, 75, 200, 1080 - 450);
            drawRect(paneRect, "#ff0");
        };

        state.cursorPointer = false;

        state.ctx.fillStyle = "#000";
        state.ctx.fillRect(0, 0, state.canvas.width, state.canvas.height);
        drawRect(rect(0, 0, 1920, 1080), "#420");

        this.grid.render();

        renderStats(0);
        renderStats(1);

        this.p1hand.render();
        this.p2hand.render();
        this.cardSelector.render();

        if (this.animatingCard) this.animatingCard.render();

        this.noCardsBanner.render();
        this.turnIndicator.render();

        this.factoryPlacer.render();
        this.siloPlacer.render();

        state.canvas.style.cursor = state.cursorPointer ? "pointer" : "default";

        state.ctx.fillStyle = "#fff";
        state.ctx.font = `10px Arial`;
        state.ctx.fillText(`${(1 / this.dt).toFixed(2)} FPS`, 8, 15);

        state.wasClickThisFrame = false;
        requestAnimationFrame(() => this.render());
    }

    async start() {
        this.turnIndicator = new TurnIndicator(this);
        this.factoryPlacer = new FactoryPlacer(this);
        this.siloPlacer = new SiloPlacer(this);
        this.grid = new Grid(this);
        this.p1hand = new Hand(this, P1);
        this.p2hand = new Hand(this, P2);
        this.cardSelector = new CardSelector(this);
        this.noCardsBanner = new NoCardsBanner(this);

        await this.initialSetup();

        this.render();
    }
}

const cardBackRed = asset("cardBackRed.png");
const cardBackBlue = asset("cardBackBlue.png");
const cardBackGreen = asset("cardBackGreen.png");
const redTile = asset("redTile.png");
const greyTile = asset("greyTile.png");
const blueTile = asset("blueTile.png");

const main = async () => {
    new Game().start();
};
main();
