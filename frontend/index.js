const BLUE = -1,
    GREY = 0,
    RED = 1;
const EMPTY = 1,
    SILO = 1,
    FACTORY = 2;
const state = {
    turn: 0,
    selectedCard: 2,
    hand: {
        0: [1, 2, 3, 4, 5, 6, 7],
        1: [1, 2, 3, 4, 5, 6, 7],
    },
    mouse: {
        x: 0,
        y: 0,
        down: false,
    },
    grid: {
        width: 20,
        height: 10,
    },
    animation: 0,
    wasClickThisFrame: false,
};

const asset = (src) => {
    const img = new Image();
    img.src = "assets/" + src;
    return img;
};

const frame = asset("frame.png");
const redTile = asset("redTile.png");
const greyTile = asset("greyTile.png");
const blueTile = asset("blueTile.png");

const main = async () => {
    const canvas = document.getElementById("root");
    /** @type {CanvasRenderingContext2D} */
    const ctx = canvas.getContext("2d");

    const start = Date.now();

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
        const { width, height } = canvas.getBoundingClientRect();
        canvas.width = width;
        canvas.height = height;
    });
    ro.observe(canvas);

    const getViewport = () => {
        const { width, height } = canvas;
        const scale = Math.min(width / 1920, height / 1080);
        return {
            xo: (width - 1920 * scale) / 2,
            yo: (height - 1080 * scale) / 2,
            scale,
        };
    };

    const rect = (x, y, w, h) => ({ x, y, w, h });
    const drawRect = ({ x, y, w, h }, colour) => {
        if (colour) ctx.fillStyle = colour;
        const { xo, yo, scale } = getViewport();
        ctx.fillRect(x * scale + xo, y * scale + yo, w * scale, h * scale);
    };
    const drawImage = ({ x, y, w, h }, image) => {
        const { xo, yo, scale } = getViewport();
        ctx.drawImage(image, x * scale + xo, y * scale + yo, w * scale, h * scale);
    };
    const collideRect = ({ x, y }, { x: rx, y: ry, w: rw, h: rh }) => {
        if (x < rx || y < ry || x >= rx + rw || y >= ry + rh) return false;
        return true;
    };

    const renderHand = (side, large) => {
        const cardWidth = large ? 200 : 100;

        const cardHeight = cardWidth * 1.4;
        const cardOverlap = cardWidth / 2;
        const hoverXOffset = cardOverlap / 2;
        const hoverYOffset = cardOverlap * 0.4;
        const selectedYOffset = cardOverlap;

        let x = side ? 1920 - 75 - cardWidth : 75;
        let y = 1080 - cardHeight - 25;

        let hoverCard = null,
            selectedCard = null,
            newSelectedNum = null;
        state.hand[side].forEach((card, n) => {
            const topCard = side ? n === 0 : n === state.hand[side].length - 1;
            const bottomCard = !side ? n === 0 : n === state.hand[side].length - 1;

            const hover = collideRect(
                state.mouse,
                rect(
                    x + side * hoverXOffset * !bottomCard,
                    y - hoverYOffset,
                    cardWidth - (topCard ? 0 : hoverXOffset),
                    cardHeight + hoverYOffset
                )
            );
            const cardRect = rect(x, y, cardWidth, cardHeight);
            const selected = n === state.selectedCard;
            if (selected) {
                cardRect.y -= selectedYOffset;
                selectedCard = cardRect;
            } else if (hover) {
                cardRect.y -= hoverYOffset;
                hoverCard = cardRect;
            } else {
                drawImage(cardRect, frame);
            }
            const step = cardWidth - cardOverlap + (hover || selected ? hoverXOffset : 0);
            if (side) x -= step;
            else x += step;

            if (state.wasClickThisFrame && hover) newSelectedNum = n;
        });
        if (newSelectedNum !== null) state.selectedCard = newSelectedNum;
        if (selectedCard) drawImage(selectedCard, frame);
        if (hoverCard) drawImage(hoverCard, frame);
    };

    const renderGrid = () => {
        const gridRect = rect(300, 50, 1920 - 600, 1080 - 400);

        const tileWidth = gridRect.w / state.grid.width;
        const tileHeight = gridRect.h / state.grid.height;
        for (let x = 0; x < state.grid.width; x++) {
            for (let y = 0; y < state.grid.height; y++) {
                tile = y % 2 === x % 2 ? redTile : blueTile;
                drawImage(rect(gridRect.x + x * tileWidth, gridRect.y + y * tileHeight, tileWidth, tileHeight), tile);
            }
        }
    };

    const renderStats = (side) => {
        const paneRect = rect(side ? 1920 - 250 : 50, 125, 200, 1080 - 350);
        drawRect(paneRect, "#ff0");
    };

    const render = () => {
        state.animation = ((Date.now() - start) / 1000) % 1;

        ctx.fillStyle = "#000";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        drawRect(rect(0, 0, 1920, 1080), "#f0f");

        renderGrid();

        renderStats(0);
        renderStats(1);

        renderHand(0, true);
        renderHand(1, false);

        state.wasClickThisFrame = false;
        requestAnimationFrame(render);
    };

    requestAnimationFrame(render);
};
main();
