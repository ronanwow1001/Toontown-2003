# File: Q (Python 2.2)

global curId
import sys
import os
import tokenize
from ShowBaseGlobal import *
from IntervalGlobal import *
import DirectNotifyGlobal
import BlinkingArrows
import ToonHeadFrame
import AvatarDNA
import Char
import Suit
import Localizer
notify = DirectNotifyGlobal.directNotify.newCategory('QuestParser')
lineDict = { }
globalVarDict = { }
curId = None

def init():
    globalVarDict.update({
        'render': render,
        'camera': camera,
        'hidden': hidden,
        'aspect2d': aspect2d,
        'localToon': toonbase.localToon,
        'laffMeter': toonbase.localToon.laffMeter,
        'inventory': toonbase.localToon.inventory,
        'bFriendsList': toonbase.localToon.bFriendsList,
        'book': toonbase.localToon.book,
        'bookPrevArrow': toonbase.localToon.book.prevArrow,
        'bookNextArrow': toonbase.localToon.book.nextArrow,
        'bookOpenButton': toonbase.localToon.book.bookOpenButton,
        'bookCloseButton': toonbase.localToon.book.bookCloseButton,
        'chatNormalButton': toonbase.localToon.chatMgr.normalButton,
        'chatQtButton': toonbase.localToon.chatMgr.qtButton,
        'arrows': BlinkingArrows.BlinkingArrows() })


def clear():
    globalVarDict.clear()


def readFile(filename):
    if vfs:
        scriptFile = StreamReader(vfs.openReadFile(filename), 1)
    else:
        scriptFile = open(filename.toOsSpecific(), 'r')
    gen = tokenize.generate_tokens(scriptFile.readline)
    line = getLineOfTokens(gen)
    while line is not None:
        if line == []:
            line = getLineOfTokens(gen)
            continue
        
        if line[0] == 'ID':
            parseId(line)
        elif curId is None:
            notify.error('Every script must begin with an ID')
        else:
            lineDict[curId].append(line)
        line = getLineOfTokens(gen)


def getLineOfTokens(gen):
    tokens = []
    nextNeg = 0
    token = gen.next()
    if token[0] == tokenize.ENDMARKER:
        return None
    
    while token[0] != tokenize.NEWLINE and token[0] != tokenize.NL:
        if token[0] == tokenize.COMMENT:
            pass
        1
        if token[0] == tokenize.OP and token[1] == '-':
            nextNeg = 1
        elif token[0] == tokenize.NUMBER:
            if nextNeg:
                tokens.append(-eval(token[1]))
                nextNeg = 0
            else:
                tokens.append(eval(token[1]))
        elif token[0] == tokenize.STRING:
            tokens.append(eval(token[1]))
        elif token[0] == tokenize.NAME:
            tokens.append(token[1])
        else:
            notify.warning('Ignored token type: %s on line: %s' % (tokenize.tok_name[token[0]], token[2][0]))
        token = gen.next()
    return tokens


def parseId(line):
    global curId
    curId = line[1]
    notify.debug('Setting current scriptId to: %s' % curId)
    if questDefined(curId):
        notify.error('Already defined scriptId: %s' % curId)
    else:
        lineDict[curId] = []


def questDefined(scriptId):
    return lineDict.has_key(scriptId)


class NPCMoviePlayer(DirectObject):
    
    def __init__(self, scriptId, toon, npc):
        self.scriptId = scriptId
        self.toon = toon
        self.isLocalToon = self.toon == toonbase.localToon
        self.npc = npc
        self.privateVarDict = { }
        self.toonHeads = { }
        self.uniqueId = 'scriptMovie_' + str(self.scriptId) + '_' + str(toon.getDoId()) + '_' + str(npc.getDoId())
        self.setVar('toon', self.toon)
        self.setVar('npc', self.npc)
        self.chapterDict = { }
        self.timeoutTrack = None
        self.currentTrack = None

    
    def getVar(self, varName):
        if self.privateVarDict.has_key(varName):
            return self.privateVarDict[varName]
        elif globalVarDict.has_key(varName):
            return globalVarDict[varName]
        else:
            notify.error('Variable not defined: %s' % varName)

    
    def delVar(self, varName):
        if self.privateVarDict.has_key(varName):
            del self.privateVarDict[varName]
        elif globalVarDict.has_key(varName):
            del globalVarDict[varName]
        else:
            notify.warning('Variable not defined: %s' % varName)

    
    def setVar(self, varName, var):
        self.privateVarDict[varName] = var

    
    def cleanup(self):
        if self.currentTrack:
            self.currentTrack.pause()
            self.currentTrack = None
        
        self.ignoreAll()
        taskMgr.remove(self.uniqueId)
        for toonHeadFrame in self.toonHeads.values():
            toonHeadFrame.destroy()
        
        del self.toonHeads
        del self.privateVarDict
        del self.chapterDict
        del self.toon
        del self.npc
        del self.timeoutTrack

    
    def timeout(self, fFinish = 0):
        if self.timeoutTrack:
            if fFinish:
                self.timeoutTrack.finish()
            else:
                self.timeoutTrack.play()
        

    
    def finishMovie(self):
        self.npc.finishMovie(self.toon, self.isLocalToon, 0.0)

    
    def playNextChapter(self, eventName, timeStamp = 0.0):
        trackList = self.chapterDict[eventName]
        if trackList:
            self.currentTrack = trackList.pop(0)
            self.currentTrack.play()
        else:
            notify.debug('Movie ended waiting for an event')

    
    def play(self):
        lineNum = 0
        self.currentEvent = 'start'
        lines = lineDict.get(self.scriptId)
        if lines is None:
            notify.error('No movie defined for scriptId: %s' % self.scriptId)
        
        chapterList = []
        timeoutList = []
        for line in lines:
            lineNum += 1
            command = line[0]
            if command == 'UPON_TIMEOUT':
                uponTimeout = 1
                iList = timeoutList
                line = line[1:]
                command = line[0]
            else:
                uponTimeout = 0
                iList = chapterList
            if command == 'CALL':
                if uponTimeout:
                    self.notify.error('CALL not allowed in an UPON_TIMEOUT')
                
                iList.append(self.parseCall(line))
                continue
            elif command == 'DEBUG':
                iList.append(self.parseDebug(line))
                continue
            elif command == 'WAIT':
                if uponTimeout:
                    self.notify.error('WAIT not allowed in an UPON_TIMEOUT')
                
                iList.append(self.parseWait(line))
                continue
            elif command == 'CHAT':
                iList.append(self.parseChat(line))
                continue
            elif command == 'CLEAR_CHAT':
                iList.append(self.parseClearChat(line))
                continue
            elif command == 'FINISH_QUEST_MOVIE':
                chapterList.append(Func(self.finishMovie))
                continue
            elif command == 'CHAT_CONFIRM':
                if uponTimeout:
                    self.notify.error('CHAT_CONFIRM not allowed in an UPON_TIMEOUT')
                
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                nextEvent = avatar.uniqueName('doneChatPage')
                iList.append(Func(self.acceptOnce, nextEvent, self.playNextChapter, [
                    nextEvent]))
                iList.append(self.parseChatConfirm(line))
                self.closePreviousChapter(iList)
                chapterList = []
                self.currentEvent = nextEvent
                continue
            elif command == 'LOCAL_CHAT_CONFIRM':
                if uponTimeout:
                    self.notify.error('LOCAL_CHAT_CONFIRM not allowed in an UPON_TIMEOUT')
                
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                nextEvent = avatar.uniqueName('doneChatPage')
                iList.append(Func(self.acceptOnce, nextEvent, self.playNextChapter, [
                    nextEvent]))
                iList.append(self.parseLocalChatConfirm(line))
                self.closePreviousChapter(iList)
                chapterList = []
                self.currentEvent = nextEvent
                continue
            elif command == 'LOCAL_CHAT_TO_CONFIRM':
                if uponTimeout:
                    self.notify.error('LOCAL_CHAT_TO_CONFIRM not allowed in an UPON_TIMEOUT')
                
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                nextEvent = avatar.uniqueName('doneChatPage')
                iList.append(Func(self.acceptOnce, nextEvent, self.playNextChapter, [
                    nextEvent]))
                iList.append(self.parseLocalChatToConfirm(line))
                self.closePreviousChapter(iList)
                chapterList = []
                self.currentEvent = nextEvent
                continue
            
            if self.isLocalToon:
                if command == 'LOAD':
                    self.parseLoad(line)
                elif command == 'LOAD_SFX':
                    self.parseLoadSfx(line)
                elif command == 'LOAD_CHAR':
                    self.parseLoadChar(line)
                elif command == 'LOAD_CLASSIC_CHAR':
                    self.parseLoadClassicChar(line)
                elif command == 'UNLOAD_CHAR':
                    iList.append(self.parseUnloadChar(line))
                elif command == 'LOAD_SUIT':
                    self.parseLoadSuit(line)
                elif command == 'SET':
                    self.parseSet(line)
                elif command == 'LOCK_LOCALTOON':
                    iList.append(self.parseLockLocalToon(line))
                elif command == 'FREE_LOCALTOON':
                    iList.append(self.parseFreeLocalToon(line))
                elif command == 'REPARENTTO':
                    iList.append(self.parseReparent(line))
                elif command == 'WRTREPARENTTO':
                    iList.append(self.parseWrtReparent(line))
                elif command == 'SHOW':
                    iList.append(self.parseShow(line))
                elif command == 'HIDE':
                    iList.append(self.parseHide(line))
                elif command == 'POS':
                    iList.append(self.parsePos(line))
                elif command == 'HPR':
                    iList.append(self.parseHpr(line))
                elif command == 'SCALE':
                    iList.append(self.parseScale(line))
                elif command == 'POSHPRSCALE':
                    iList.append(self.parsePosHprScale(line))
                elif command == 'COLOR':
                    iList.append(self.parseColor(line))
                elif command == 'COLOR_SCALE':
                    iList.append(self.parseColorScale(line))
                elif command == 'ADD_LAFFMETER':
                    iList.append(self.parseAddLaffMeter(line))
                elif command == 'LAFFMETER':
                    iList.append(self.parseLaffMeter(line))
                elif command == 'OBSCURE_LAFFMETER':
                    iList.append(self.parseObscureLaffMeter(line))
                elif command == 'ARROWS_ON':
                    iList.append(self.parseArrowsOn(line))
                elif command == 'ARROWS_OFF':
                    iList.append(self.parseArrowsOff(line))
                elif command == 'SHOW_FRIENDS_LIST':
                    iList.append(self.parseShowFriendsList(line))
                elif command == 'HIDE_FRIENDS_LIST':
                    iList.append(self.parseHideFriendsList(line))
                elif command == 'SHOW_BOOK':
                    iList.append(self.parseShowBook(line))
                elif command == 'HIDE_BOOK':
                    iList.append(self.parseHideBook(line))
                elif command == 'OBSCURE_BOOK':
                    iList.append(self.parseObscureBook(line))
                elif command == 'OBSCURE_CHAT':
                    iList.append(self.parseObscureChat(line))
                elif command == 'ADD_INVENTORY':
                    iList.append(self.parseAddInventory(line))
                elif command == 'SET_INVENTORY':
                    iList.append(self.parseSetInventory(line))
                elif command == 'SET_INVENTORY_YPOS':
                    iList.append(self.parseSetInventoryYPos(line))
                elif command == 'SET_INVENTORY_DETAIL':
                    iList.append(self.parseSetInventoryDetail(line))
                elif command == 'PLAY_SFX':
                    iList.append(self.parsePlaySfx(line))
                elif command == 'STOP_SFX':
                    iList.append(self.parseStopSfx(line))
                elif command == 'PLAY_ANIM':
                    iList.append(self.parsePlayAnim(line))
                elif command == 'LOOP_ANIM':
                    iList.append(self.parseLoopAnim(line))
                elif command == 'LERP_POS':
                    iList.append(self.parseLerpPos(line))
                elif command == 'LERP_HPR':
                    iList.append(self.parseLerpHpr(line))
                elif command == 'LERP_SCALE':
                    iList.append(self.parseLerpScale(line))
                elif command == 'LERP_POSHPRSCALE':
                    iList.append(self.parseLerpPosHprScale(line))
                elif command == 'LERP_COLOR':
                    iList.append(self.parseLerpColor(line))
                elif command == 'LERP_COLOR_SCALE':
                    iList.append(self.parseLerpColorScale(line))
                elif command == 'DEPTH_WRITE_ON':
                    iList.append(self.parseDepthWriteOn(line))
                elif command == 'DEPTH_WRITE_OFF':
                    iList.append(self.parseDepthWriteOff(line))
                elif command == 'DEPTH_TEST_ON':
                    iList.append(self.parseDepthTestOn(line))
                elif command == 'DEPTH_TEST_OFF':
                    iList.append(self.parseDepthTestOff(line))
                elif command == 'TOON_HEAD':
                    iList.append(self.parseToonHead(line))
                elif command == 'SEND_EVENT':
                    iList.append(self.parseSendEvent(line))
                elif command == 'FUNCTION':
                    iList.append(self.parseFunction(line))
                elif command == 'WAIT_EVENT':
                    if uponTimeout:
                        self.notify.error('WAIT_EVENT not allowed in an UPON_TIMEOUT')
                    
                    nextEvent = self.parseWaitEvent(line)
                    iList.append(Func(self.acceptOnce, nextEvent, self.playNextChapter, [
                        nextEvent]))
                    self.closePreviousChapter(iList)
                    chapterList = []
                    self.currentEvent = nextEvent
                else:
                    notify.warning('Unknown command token: %s for scriptId: %s on line: %s' % (command, self.scriptId, lineNum))
            
        
        self.closePreviousChapter(chapterList)
        if timeoutList:
            self.timeoutTrack = Track(timeoutList, name = 'Quest-movie-timeout')
        
        self.playNextChapter('start')

    
    def closePreviousChapter(self, iList):
        trackList = self.chapterDict.setdefault(self.currentEvent, [])
        trackList.append(Track(iList))

    
    def parseLoad(self, line):
        if len(line) == 3:
            (token, varName, modelPath) = line
            node = loader.loadModel(modelPath)
        elif len(line) == 4:
            (token, varName, modelPath, subNodeName) = line
            node = loader.loadModel(modelPath).find('**/' + subNodeName)
        else:
            notify.error('invalid parseLoad command')
        self.setVar(varName, node)
        return None

    
    def parseLoadSfx(self, line):
        (token, varName, fileName) = line
        sfx = base.loadSfx(fileName)
        self.setVar(varName, sfx)
        return None

    
    def parseLoadChar(self, line):
        (token, name, charType) = line
        char = Char.Char()
        dna = AvatarDNA.AvatarDNA()
        dna.newChar(charType)
        char.setDNA(dna)
        if charType == 'mk' or charType == 'mn':
            char.startEarTask()
        
        char.nametag.manage(toonbase.marginManager)
        char.addActive()
        char.hideName()
        self.setVar(name, char)

    
    def parseLoadClassicChar(self, line):
        (token, name) = line
        char = Char.Char()
        dna = AvatarDNA.AvatarDNA()
        if self.toon.getStyle().gender == 'm':
            charType = 'mk'
        else:
            charType = 'mn'
        dna.newChar(charType)
        char.setDNA(dna)
        char.startEarTask()
        char.nametag.manage(toonbase.marginManager)
        char.addActive()
        char.hideName()
        self.setVar(name, char)

    
    def parseUnloadChar(self, line):
        (token, name) = line
        char = self.getVar(name)
        iList = []
        iList.append(Func(char.removeActive))
        if char.style.name == 'mk' or char.style.name == 'mn':
            iList.append(Func(char.stopEarTask))
        
        iList.append(Func(char.delete))
        iList.append(Func(self.delVar, name))
        return Sequence(iList)

    
    def parseLoadSuit(self, line):
        (token, name, suitType) = line
        suit = Suit.Suit()
        dna = AvatarDNA.AvatarDNA()
        dna.newSuit(suitType)
        suit.setDNA(dna)
        self.setVar(name, suit)

    
    def parseSet(self, line):
        (token, varName, value) = line
        self.setVar(varName, value)
        return None

    
    def parseCall(self, line):
        (token, scriptId) = line
        nmp = NPCMoviePlayer(scriptId, self.toon, self.npc)
        return Func(nmp.play)

    
    def parseLockLocalToon(self, line):
        return Sequence(Func(self.toon.detachCamera), Func(self.toon.stopTrackAnimToSpeed), Func(self.toon.stopUpdateSmartCamera))

    
    def parseFreeLocalToon(self, line):
        return Sequence(Func(self.toon.attachCamera), Func(self.toon.startTrackAnimToSpeed), Func(self.toon.startUpdateSmartCamera))

    
    def parseDebug(self, line):
        (token, str) = line
        return Func(notify.debug, str)

    
    def parseReparent(self, line):
        if len(line) == 3:
            (token, childNodeName, parentNodeName) = line
            subNodeName = None
        elif len(line) == 4:
            (token, childNodeName, parentNodeName, subNodeName) = line
        
        childNode = self.getVar(childNodeName)
        if subNodeName:
            parentNode = self.getVar(parentNodeName).find(subNodeName)
        else:
            parentNode = self.getVar(parentNodeName)
        return ParentInterval(childNode, parentNode)

    
    def parseWrtReparent(self, line):
        if len(line) == 3:
            (token, childNodeName, parentNodeName) = line
            subNodeName = None
        elif len(line) == 4:
            (token, childNodeName, parentNodeName, subNodeName) = line
        
        childNode = self.getVar(childNodeName)
        if subNodeName:
            parentNode = self.getVar(parentNodeName).find(subNodeName)
        else:
            parentNode = self.getVar(parentNodeName)
        return WrtParentInterval(childNode, parentNode)

    
    def parseShow(self, line):
        (token, nodeName) = line
        node = self.getVar(nodeName)
        return Func(node.show)

    
    def parseHide(self, line):
        (token, nodeName) = line
        node = self.getVar(nodeName)
        return Func(node.hide)

    
    def parsePos(self, line):
        (token, nodeName, x, y, z) = line
        node = self.getVar(nodeName)
        return Func(node.setPos, x, y, z)

    
    def parseHpr(self, line):
        (token, nodeName, h, p, r) = line
        node = self.getVar(nodeName)
        return Func(node.setHpr, h, p, r)

    
    def parseScale(self, line):
        (token, nodeName, x, y, z) = line
        node = self.getVar(nodeName)
        return Func(node.setScale, x, y, z)

    
    def parsePosHprScale(self, line):
        (token, nodeName, x, y, z, h, p, r, sx, sy, sz) = line
        node = self.getVar(nodeName)
        return Func(node.setPosHprScale, x, y, z, h, p, r, sx, sy, sz)

    
    def parseColor(self, line):
        (token, nodeName, r, g, b, a) = line
        node = self.getVar(nodeName)
        return Func(node.setColor, r, g, b, a)

    
    def parseColorScale(self, line):
        (token, nodeName, r, g, b, a) = line
        node = self.getVar(nodeName)
        return Func(node.setColorScale, r, g, b, a)

    
    def parseWait(self, line):
        (token, waitTime) = line
        return Wait(waitTime)

    
    def parseChat(self, line):
        toonId = self.toon.getDoId()
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval('Localizer.' + line[2])
        if len(line) == 3:
            chatFlags = CFSpeech | CFTimeout
        else:
            extraChatFlag = eval(line[3])
            chatFlags = CFSpeech | CFTimeout | extraChatFlag
        return Func(avatar.setChatAbsolute, chatString, chatFlags)

    
    def parseClearChat(self, line):
        toonId = self.toon.getDoId()
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatFlags = CFSpeech | CFTimeout
        return Func(avatar.setChatAbsolute, '', chatFlags)

    
    def parseChatConfirm(self, line):
        toonId = self.toon.getDoId()
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval('Localizer.' + line[2])
        if len(line) == 3:
            quitButton = 0
            extraChatFlags = None
        elif len(line) == 4:
            arg = line[3]
            if type(arg) == type(0):
                quitButton = line[3]
                extraChatFlags = None
            elif type(arg) == type(''):
                quitButton = 0
                extraChatFlags = eval(line[3])
            else:
                notify.error('invalid argument type')
        elif len(line) == 5:
            quitButton = line[3]
            extraChatFlags = eval(line[4])
        else:
            notify.error('invalid number of arguments')
        return Func(avatar.setPageChat, toonId, 0, chatString, quitButton, extraChatFlags)

    
    def parseLocalChatConfirm(self, line):
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval('Localizer.' + line[2])
        if len(line) == 3:
            quitButton = 0
            extraChatFlags = None
        elif len(line) == 4:
            arg = line[3]
            if type(arg) == type(0):
                quitButton = line[3]
                extraChatFlags = None
            elif type(arg) == type(''):
                quitButton = 0
                extraChatFlags = eval(line[3])
            else:
                notify.error('invalid argument type')
        elif len(line) == 5:
            quitButton = line[3]
            extraChatFlags = eval(line[4])
        else:
            notify.error('invalid number of arguments')
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags)

    
    def parseLocalChatToConfirm(self, line):
        avatarKey = line[1]
        avatar = self.getVar(avatarKey)
        toAvatarKey = line[2]
        toAvatar = self.getVar(toAvatarKey)
        toAvatarName = toAvatar.name.capitalize()
        chatString = eval('Localizer.' + line[3])
        chatString = chatString.replace('%s', toAvatarName)
        if len(line) == 4:
            quitButton = 0
            extraChatFlags = None
        elif len(line) == 5:
            arg = line[4]
            if type(arg) == type(0):
                quitButton = line[4]
                extraChatFlags = None
            elif type(arg) == type(''):
                quitButton = 0
                extraChatFlags = eval(line[4])
            else:
                notify.error('invalid argument type')
        elif len(line) == 6:
            quitButton = line[4]
            extraChatFlags = eval(line[5])
        else:
            notify.error('invalid number of arguments')
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags)

    
    def parsePlaySfx(self, line):
        if len(line) == 2:
            (token, sfxName) = line
        elif len(line) == 3:
            (token, sfxName, looping) = line
        else:
            notify.error('invalid number of arguments')
        sfx = self.getVar(sfxName)
        return Func(base.playSfx, sfx, looping)

    
    def parseStopSfx(self, line):
        (token, sfxName) = line
        sfx = self.getVar(sfxName)
        return Func(sfx.stop)

    
    def parsePlayAnim(self, line):
        if len(line) == 3:
            (token, actorName, animName) = line
            playRate = 1.0
        elif len(line) == 4:
            (token, actorName, animName, playRate) = line
        else:
            notify.error('invalid number of arguments')
        actor = self.getVar(actorName)
        return Sequence(Func(actor.setPlayRate, playRate, animName), Func(actor.play, animName))

    
    def parseLoopAnim(self, line):
        if len(line) == 3:
            (token, actorName, animName) = line
            playRate = 1.0
        elif len(line) == 4:
            (token, actorName, animName, playRate) = line
        else:
            notify.error('invalid number of arguments')
        actor = self.getVar(actorName)
        return Sequence(Func(actor.setPlayRate, playRate, animName), Func(actor.loop, animName))

    
    def parseLerpPos(self, line):
        (token, nodeName, x, y, z, t) = line
        node = self.getVar(nodeName)
        return Sequence(LerpPosInterval(node, t, Point3(x, y, z), blendType = 'easeInOut'), duration = 0.0)

    
    def parseLerpHpr(self, line):
        (token, nodeName, h, p, r, t) = line
        node = self.getVar(nodeName)
        return Sequence(LerpHprInterval(node, t, VBase3(h, p, r), blendType = 'easeInOut'), duration = 0.0)

    
    def parseLerpScale(self, line):
        (token, nodeName, x, y, z, t) = line
        node = self.getVar(nodeName)
        return Sequence(LerpScaleInterval(node, t, VBase3(x, y, z), blendType = 'easeInOut'), duration = 0.0)

    
    def parseLerpPosHprScale(self, line):
        (token, nodeName, x, y, z, h, p, r, sx, sy, sz, t) = line
        node = self.getVar(nodeName)
        return Sequence(LerpPosHprScaleInterval(node, t, VBase3(x, y, z), VBase3(h, p, r), VBase3(sx, sy, sz), blendType = 'easeInOut'), duration = 0.0)

    
    def parseLerpColor(self, line):
        (token, nodeName, sr, sg, sb, sa, er, eg, eb, ea, t) = line
        node = self.getVar(nodeName)
        return Sequence(LerpColorInterval(node, t, VBase4(er, eg, eb, ea), startColorScale = VBase4(sr, sg, sb, sa), blendType = 'easeInOut'), duration = 0.0)

    
    def parseLerpColorScale(self, line):
        (token, nodeName, sr, sg, sb, sa, er, eg, eb, ea, t) = line
        node = self.getVar(nodeName)
        return Sequence(LerpColorScaleInterval(node, t, VBase4(er, eg, eb, ea), startColorScale = VBase4(sr, sg, sb, sa), blendType = 'easeInOut'), duration = 0.0)

    
    def parseDepthWriteOn(self, line):
        (token, nodeName, depthWrite) = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.setDepthWrite, depthWrite))

    
    def parseDepthWriteOff(self, line):
        (token, nodeName) = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.clearDepthWrite))

    
    def parseDepthTestOn(self, line):
        (token, nodeName, depthTest) = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.setDepthTest, depthTest))

    
    def parseDepthTestOff(self, line):
        (token, nodeName) = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.clearDepthTest))

    
    def parseWaitEvent(self, line):
        (token, eventName) = line
        return eventName

    
    def parseSendEvent(self, line):
        (token, eventName) = line
        return Func(messenger.send, eventName)

    
    def parseFunction(self, line):
        (token, objectName, functionName) = line
        object = self.getVar(objectName)
        cfunc = compile('object' + '.' + functionName, '<string>', 'eval')
        return Func(eval(cfunc))

    
    def parseAddLaffMeter(self, line):
        (token, maxHpDelta) = line
        newMaxHp = maxHpDelta + self.toon.getMaxHp()
        newHp = newMaxHp
        laffMeter = self.getVar('laffMeter')
        return Func(laffMeter.adjustFace, newHp, newMaxHp)

    
    def parseLaffMeter(self, line):
        (token, newHp, newMaxHp) = line
        laffMeter = self.getVar('laffMeter')
        return Func(laffMeter.adjustFace, newHp, newMaxHp)

    
    def parseObscureLaffMeter(self, line):
        (token, val) = line
        return Func(self.toon.laffMeter.obscure, val)

    
    def parseAddInventory(self, line):
        (token, track, level, number) = line
        inventory = self.getVar('inventory')
        countSound = base.loadSfx('phase_3.5/audio/sfx/tick_counter.mp3')
        return Sequence(Func(base.playSfx, countSound), Func(inventory.buttonBoing, track, level), Func(inventory.addItems, track, level, number), Func(inventory.updateGUI, track, level))

    
    def parseSetInventory(self, line):
        (token, track, level, number) = line
        inventory = self.getVar('inventory')
        return Sequence(Func(inventory.setItem, track, level, number), Func(inventory.updateGUI, track, level))

    
    def parseSetInventoryYPos(self, line):
        (token, track, level, yPos) = line
        inventory = self.getVar('inventory')
        button = inventory.buttons[track][level].stateNodePath[0]
        text = button.find('**/+TextNode')
        return Sequence(Func(text.setY, yPos))

    
    def parseSetInventoryDetail(self, line):
        if len(line) == 2:
            (token, val) = line
        elif len(line) == 4:
            (token, val, track, level) = line
        else:
            notify.error('invalid line for parseSetInventoryDetail: %s' % line)
        inventory = self.getVar('inventory')
        if val == -1:
            return Func(inventory.noDetail)
        elif val == 0:
            return Func(inventory.hideDetail)
        elif val == 1:
            return Func(inventory.showDetail, track, level)
        else:
            notify.error('invalid inventory detail level: %s' % val)

    
    def parseShowFriendsList(self, line):
        import FriendsListPanel
        return Func(FriendsListPanel.showFriendsList)

    
    def parseHideFriendsList(self, line):
        import FriendsListPanel
        return Func(FriendsListPanel.hideFriendsList)

    
    def parseShowBook(self, line):
        return Sequence(Func(self.toon.book.setPage, self.toon.mapPage), Func(self.toon.book.enter))

    
    def parseHideBook(self, line):
        return Func(self.toon.book.exit)

    
    def parseObscureBook(self, line):
        (token, val) = line
        return Func(self.toon.book.obscureButton, val)

    
    def parseObscureChat(self, line):
        (token, val0, val1) = line
        return Func(self.toon.chatMgr.obscure, val0, val1)

    
    def parseArrowsOn(self, line):
        arrows = self.getVar('arrows')
        (token, x1, y1, h1, x2, y2, h2) = line
        return Func(arrows.arrowsOn, x1, y1, h1, x2, y2, h2)

    
    def parseArrowsOff(self, line):
        arrows = self.getVar('arrows')
        return Func(arrows.arrowsOff)

    
    def parseToonHead(self, line):
        (token, toonName, x, z, toggle) = line
        toon = self.getVar(toonName)
        toonId = toon.getDoId()
        toonHeadFrame = self.toonHeads.get(toonId)
        if not toonHeadFrame:
            toonHeadFrame = ToonHeadFrame.ToonHeadFrame(toon)
            toonHeadFrame.tag1Node.setActive(1)
            toonHeadFrame.hide()
            self.toonHeads[toonId] = toonHeadFrame
        
        if toggle:
            return Sequence(Func(toonHeadFrame.setPos, x, 0, z), Func(toonHeadFrame.show))
        else:
            return Func(toonHeadFrame.hide)


searchPath = DSearchPath()
searchPath.appendDirectory(Filename('phase_3/etc'))
searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TOONTOWN/src/quest')))
scriptFile = Filename('QuestScripts.txt')
if vfs:
    found = vfs.resolveFilename(scriptFile, searchPath)
else:
    found = scriptFile.resolveFilename(searchPath)
if not found:
    notify.error('Could not find QuestScripts.txt file')

readFile(scriptFile)
