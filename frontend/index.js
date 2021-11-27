const P1 = 1,
    P2 = 2;
const BLUE = -1,
    GREY = 0,
    RED = 1;
const EMPTY = 1,
    SILO = 1,
    FACTORY = 2;
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

const SHAPES = {
    [BOMB_SQUARE]: [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1],
    ],
    [BOMB_CIRCLE]: [
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
    ],
    [BOMB_DIAMOND]: [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ],
    [BOMB_TARGET]: [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ],
    [BOMB_DOT_DOT_DOT]: [
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
    ],
    [BOMB_X]: [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ],
    [BOMB_H_BOMB]: [
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    [BOMB_P_BOMB]: [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    [BOMB_CHERRY]: [
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
    ],
    [BOMB_E]: [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 0, 1],
    ],
    [BOMB_A_BOMB]: [
        [0, 0, 0, 1, 1],
        [0, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1],
    ],
    [BOMB_ENGLAND]: [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
};

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

const randomCardType = () => {
    const rand = Math.random();
    return Math.floor(rand * 9) + 1;
};

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
const drawText = (x, y, text, size, colour) => {
    const { xo, yo, scale } = getViewport();
    state.ctx.drawText((x + xo) * scale, (y + yo) * scale, text, size * scale, colour);
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
        this.image = null;
        this.rect = rect;
        this._rect = { ...rect };
        this.scale = 1;
        this.rotation = 0;
        this.animateScale = false;
        this.animateRotataion = false;
        this.animatePos = false;
    }
    setScale(scale) {
        this.scale = scale;
        if (false && !this.animateScale) this._scale = this.scale;
    }
    setRotation(rotation) {
        this.rotation = rotation;
        if (!this.animateRotataion) this._rotation = this.rotation;
    }
    setRect(rect) {
        this.rect = { ...rect };
    }
    render() {
        this._scale = step(this._scale, this.scale);
        this._rotation = step(this._rotation, this.rotation);
        if (this.animatePos) {
            this._rect.x = step(this._rect.x, this.rect.x);
            this._rect.y = step(this._rect.y, this.rect.y);
            this._rect.w = step(this._rect.w, this.rect.w);
            this._rect.h = step(this._rect.h, this.rect.h);
        } else this._rect = this.rect;

        if (this.image) drawImage(this._rect, this.image, this._rotation, this._scale);
    }
}

class Tile extends Entity {
    constructor(rect, type) {
        super(rect);
        this.animateScale = true;
        this.image = type === RED ? redTile : type === BLUE ? blueTile : greyTile;
    }
}

class Card extends Entity {
    constructor(rect, bombId) {
        super(rect);
        bombId = randomCardType();
        this.bombId = bombId;
        this.image = bombId === -1 ? cardBackRed : CARDS[bombId];
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

        for (let i = 0; i < 50; i++) this.addCard(player === P1 ? 0 : -1);
    }
    addCard(type) {
        this.cards.push(new Card(rect(), type));
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

        this.active = true;
    }

    newSelection(choices) {
        this.cards = [];
        choices.forEach((x) => this.addCard(x));
    }

    addCard(type) {
        const card = new Card(rect(), type);
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
                const rand = Math.random();
                this.tiles[x].push(
                    new Tile(
                        rect(
                            this.RECT.x + x * this.TILE_WIDTH,
                            this.RECT.y + y * this.TILE_HEIGHT,
                            this.TILE_WIDTH,
                            this.TILE_HEIGHT
                        ),
                        rand > 0.66 ? RED : rand > 0.33 ? BLUE : GREY
                    )
                );
            }
        }
    }

    render() {
        let hoverTile = null;
        this.tiles.forEach((col, x) => {
            col.forEach((tile, y) => {
                tile.render();
                const hover = collideRect(state.mouse, tile.rect);
                if (hover) hoverTile = [x, y];
                tile.setScale(1);

                if (hover && this.game.selectedCard && state.wasClickThisFrame) this.game.playCard(x, y);
            });
        });

        const hovers = [];
        if (hoverTile && this.game.selectedCard !== null) {
            state.cursorPointer = true;
            for (let dx = 0; dx < 5; dx++) {
                for (let dy = 0; dy < 5; dy++) {
                    if (this.game.selectedBombShape[dx][dy]) {
                        hovers.push([hoverTile[0] + dx - 2, hoverTile[1] + dy - 2]);
                    }
                }
            }
        }

        for (const [x, y] of hovers) {
            this.tiles[x]?.[y]?.setScale(0.5);
        }
    }
}

class Game {
    constructor() {
        this.grid = new Grid(this);
        this.player = P1;
        this.p1Hand = new Hand(this, P1);
        this.p2Hand = new Hand(this, P2);
        this.cardSelector = new CardSelector(this);

        this.selectedBombShape = null;
        this.selectionActive = true;

        this.selectedCard = null;

        state.canvas = document.getElementById("root");
        /** @type {CanvasRenderingContext2D} */
        state.ctx = state.canvas.getContext("2d");

        this.startTime = Date.now();
        this.lastFrame = this.startTime;
        this.dt = 0;
        this.setupListeners();

        this.newHand();
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

    async playCard(x, y) {
        if (!this.selectedCard) return;
        state.wasClickThisFrame = false;
        await post("place_bomb", {
            player: this.player,
            coords: [x, y],
            bombId: this.selectedCard.bombId,
        });
        this.p1Hand.cards = this.p1Hand.cards.filter((x) => x !== this.selectedCard);
        this.selectedCard = null;
        this.selectionActive = false;

        // const gameState = await post("get_game_state", { player: this.player });

        // await delay(500);
    }

    async newHand() {
        const handOptions = await post("get_hand_options", { player: this.player });
        if (handOptions && handOptions.length !== 0) {
            this.cardSelector.newSelection(handOptions);
            this.cardSelector.active = true;
        }
    }

    async chooseNewCard(card) {
        state.wasClickThisFrame = false;

        await post("get_hand_options", {
            player: this.player,
            bombId: card.bombId,
        });

        this.p1Hand.cards.push(card);
        this.cardSelector.active = false;
        this.selectedCard = null;
        this.selectionActive = true;
    }

    selectCard(card) {
        this.selectedCard = card;
        if (card) this.selectedBombShape = SHAPES[card.bombId];
    }

    updateTiming() {
        // Timing code
        const now = Date.now();
        state.animation = (now - this.startTime) / 1000;
        this.dt = (now - this.lastFrame) / 1000;
        this.lastFrame = now;
    }

    render() {
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

        this.p1Hand.render();
        this.p2Hand.render();

        this.cardSelector.render();

        state.canvas.style.cursor = state.cursorPointer ? "pointer" : "default";

        state.ctx.fillStyle = "#fff";
        state.ctx.fillText(`${(1 / this.dt).toFixed(2)} FPS`, 10, 10);

        state.wasClickThisFrame = false;
        requestAnimationFrame(() => this.render());
    }

    start() {
        this.render();
    }
}

const cardBackRed = asset("cardBackRed.png");
const cardBackBlue = asset("cardBackBlue.png");
const cardBackGreen = asset("cardBackGreen.png");
const redTile = asset("redTile.png");
const greyTile = asset("greyTile.png");
const blueTile = asset("blueTile.png");

const CARDS = {
    [BOMB_SQUARE]: asset("cards/1.png"),
    [BOMB_CIRCLE]: asset("cards/2.png"),
    [BOMB_DIAMOND]: asset("cards/3.png"),
    [BOMB_TARGET]: asset("cards/4.png"),
    [BOMB_DOT_DOT_DOT]: asset("cards/5.png"),
    [BOMB_X]: asset("cards/6.png"),
    [BOMB_H_BOMB]: asset("cards/7.png"),
    [BOMB_P_BOMB]: asset("cards/8.png"),
    [BOMB_CHERRY]: asset("cards/9.png"),
};

const main = async () => {
    new Game().start();
};
main();
