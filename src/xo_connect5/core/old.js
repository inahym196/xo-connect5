'use strict';
const SERVER_PORT = 8080;
const REDIS_PORT = 6379;
const REDIS_HOST = "0.0.0.0";
const PUBLIC_DIR = __dirname + "/public";

const express = require('express');
const http = require('http');
const socketIO = require("socket.io");
const redis = require('redis');
const serverFunc = require('./internal/serverFunctions');

const app = express();
const server = http.Server(app);
const io = socketIO(server);
const redisClient = redis.createClient(REDIS_PORT, REDIS_HOST);
const PORT = process.env.PORT || SERVER_PORT;
//const HOST = '0.0.0.0';

app.use('/', express.static(PUBLIC_DIR));

app.get('/', (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

io.on("connection", (socket) => {
    //console.log("user has connected.");
    socket.on("join-room", (joinRoomValue) => {
        let room = joinRoomValue.roomName;
        if (room.length < 1 || 12 < room.length) return;
        socket.join(room);
        console.log("join (" + room + ") " + socket.id + "\n"); // + new Date());
        console.log("---------------------------------");
        let roomMember = Array.from(io.in(room).adapter.sids.keys());
        console.log(roomMember, roomMember.length);
        if (roomMember.length === 1) {
            let roomObject = {};
            roomObject.pieces = serverFunc.initPieces();
            //console.log(roomObject.pieces);
            roomObject.players = [socket.id];
            roomObject.player_putcount = [0, 0];
            roomObject.turn = 0;
            redisClient.set(room, JSON.stringify(roomObject));
            io.to(room).emit("change-mode", {
                mode: "wait",
                turn: 0
            });
            console.log("player waiting...");
        } else if (roomMember.length === 2) {
            io.to(room).emit("change-mode", {
                mode: "start",
                turn: 1
            });
            console.log("buttle start!");
            redisClient.get(room, (_, value) => {
                let roomObject = JSON.parse(value);
                roomObject.players.push(socket.id);
                console.log(roomObject.players);
                io.to(room).emit("update-pieces", {
                    pieces: roomObject.pieces,
                    nextTurn: 0,
                    winnerID: 0
                });
                redisClient.set(room, JSON.stringify(roomObject));
            });
        } else {
            io.to(room).emit("over-notice");
            socket.leaveAll();
        }

        socket.on("put-piece", (value) => {
            let x = value.x;
            let y = value.y;
            const NumGrid = 9;
            if (x < 0 || NumGrid < x || y < 0 || NumGrid < y) return;
            redisClient.get(room, (_, value) => {
                let roomObject = JSON.parse(value);
                let nextTurn = roomObject.turn === 0 ? 1 : 0;
                let setPiece = roomObject.players.indexOf(socket.id) === 1 ? 2 : 1;
                //let reversePiece = setPiece === 1 ? 2 : 1;
                //let reversed = false;
                let pass = true;
                if (
                    roomObject.players.indexOf(socket.id) === roomObject.turn &&
                    roomObject.pieces[y][x] === 0
                ) {
                    roomObject.player_putcount[roomObject.turn] += 1;
                    if (roomObject.player_putcount[roomObject.turn] % 4 === 0) {
                        roomObject.pieces[y][x] = setPiece + 2;
                    } else {
                        roomObject.pieces[y][x] = setPiece;
                    };
                    let winnerID = serverFunc.judgeStraightFive(roomObject.pieces, y, x, setPiece);
                    if (winnerID === 1) {
                        winnerID = roomObject.turn + 1;
                    };
                    // ターン切替え
                    //if (pass) nextTurn = roomObject.turn;
                    roomObject.turn = nextTurn;
                    io.to(room).emit("update-pieces", {
                        pieces: roomObject.pieces,
                        nextTurn: nextTurn,
                        winnerID: winnerID
                    });
                    redisClient.set(room, JSON.stringify(roomObject));
                }
            });
        });
        socket.on("disconnect", (disconnectvalue) => {
            console.log("exit (" + room + ") " + socket.id + "\n"); // + new date());
            console.log("---------------------------------");
            // クライアント取得
            let roomMember = Array.from(io.in(room).adapter.sids.keys());
            if (roomMember.length === 0) {
                // ルーム削除
                console.log("delete room", room);
                redisClient.del(room);
            } else if (roomMember.length === 1) {
                // 待機
                // コマ初期化
                redisClient.get(room, (_, value) => {
                    let roomObject = JSON.parse(value);
                    roomObject.pieces = serverFunc.initPieces();
                    roomObject.players.splice(roomObject.players.indexOf(socket.id), 1);
                    roomObject.turn = 0;
                    roomObject.player_putcount = [0, 0];
                    redisClient.set(room, JSON.stringify(roomObject));
                });
                // モード通知
                io.to(room).emit("change-mode", {
                    mode: "wait",
                    turn: 0
                });
            }
            socket.leaveAll();
        });
    });
});

server.listen(PORT);