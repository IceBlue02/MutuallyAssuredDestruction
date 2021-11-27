const P1 = 0,
    P2 = 1;
const BLUE = -1,
    GREY = 0,
    RED = 1;
const EMPTY = 1,
    SILO = 1,
    FACTORY = 2;
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
    constructor(rect, player) {
        super(rect);
        const rand = Math.random();
        this.image = rand > 0.66 ? cardBackRed : rand > 0.33 ? cardBackBlue : cardBackGreen;
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

        for (let i = 0; i < 10; i++) this.addCard();
    }
    addCard() {
        this.cards.push(new Card(rect(), this.player));
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
            newSelectedNum = null;
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

            if (state.wasClickThisFrame && isP1 && hover) newSelectedNum = card;
        });

        if (newSelectedNum !== null) {
            if (newSelectedNum === this.game.selectedCard) this.game.selectedCard = null;
            else this.game.selectedCard = newSelectedNum;
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

        this.cardWidth = 150;
        this.cardHeight = this.cardWidth * 1.4;
        this.cardGap = 15;

        this.newSelection();
    }

    newSelection() {
        this.cards = [];
        for (let i = 0; i < 10; i++) this.addCard();
    }

    addCard() {
        const card = new Card(rect(), P1);
        this.cards.push(card);
        card.animateScale = false;
        card.setScale(0);
        card.animateScale = true;
    }

    render() {
        if (!this.active) return;

        const width = this.cards.length * this.cardWidth + (this.cards.length - 1) * this.cardGap;
        let x = (1920 - width) / 2;
        let y = (1080 - this.cardHeight) / 2 - 50;

        for (const card of this.cards) {
            card.rect = rect(x, y, this.cardWidth, this.cardHeight);
            const hover = collideRect(state.mouse, card.rect);
            if (hover && state.wasClickThisFrame) this.game.chooseNewCard(card);
            card.render();
            card.setScale(hover ? 1.1 : 1);
            card.setRotation(hover ? tween(2) * 2 : 0);
            if (hover) state.cursorPointer = true;
            x += this.cardWidth + this.cardGap;
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
        this.p1Hand = new Hand(this, P1);
        this.p2Hand = new Hand(this, P2);
        this.cardSelector = new CardSelector(this);

        this.selectedBombShape = [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
        ];
        this.selectionActive = false;

        this.selectedCard = null;

        state.canvas = document.getElementById("root");
        /** @type {CanvasRenderingContext2D} */
        state.ctx = state.canvas.getContext("2d");

        this.startTime = Date.now();
        this.lastFrame = this.startTime;
        this.dt = 0;
        this.setupListeners();
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

    playCard(card, x, y) {
        if (!this.selectedCard) return;
        state.wasClickThisFrame = false;
        // TODO: This
        this.p1Hand.cards = this.p1Hand.cards.filter((x) => x !== this.selectedCard);
        this.selectedCard = null;
        this.selectionActive = false;
        this.cardSelector.active = true;
    }

    chooseNewCard(card) {
        state.wasClickThisFrame = false;
        // TODO: This
        this.p1Hand.cards.push(card);
        this.cardSelector.active = false;
        this.selectedCard = null;
        this.cardSelector.newSelection();
        this.selectionActive = true;
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

const main = async () => {
    new Game().start();
};
main();
