import scrython, re, sys


def cards(input):
    print(f"DEBUG {input}")
    match = re.findall(r'\[\[(.*?)\]\]', input)
    # asyncio.set_event_loop(asyncio.new_event_loop())
    is_flipcard = False
    photos = []
    button_list = []
    footer_list = []
    header_list = []
    for index, name in enumerate(match):
        print(f"DEBUG looking for: {name}")
        if index > 6:
            break
        try:
            print(f"DEBUG asking scryfall for: {name}")
            card = scrython.cards.Named(fuzzy=name)
            print(f"DEBUG scryfall answer received for: {name}")
        except scrython.ScryfallError:
            print(f"DEBUG scryfall error for: {name}")
            auto = scrython.cards.Autocomplete(q=name, query=name)
            if len(auto.data()) > 0:
                if len(auto.data()) == 1:
                    uniquename = auto.data()[0]
                    print(f"DEBUG found autocomplete with one name: {uniquename}")
                    card = scrython.cards.Named(fuzzy=uniquename)
                    print(f'DEBUG found new info for: {uniquename}')
                else:
                    text = ""
                    for index, item in zip(range(5), auto.data()):
                        text += '`{}`\n'.format(item)
                    # context.bot.send_message(chat_id=update.message.chat_id,
                    #                          text=strings.Card.card_autocorrect.format(text),
                    #                          parse_mode=telegram.ParseMode.MARKDOWN)
                    print(f'DEBUG AUTOCORRECT: {text}')
                    continue
            else:
                # context.bot.send_message(chat_id=update.message.chat_id,
                #                          text=strings.Card.card_not_found.format(name),
                #                          parse_mode=telegram.ParseMode.MARKDOWN)
                print(f'DEBUG CARD NOT FOUND: {name}')
                continue
     

        legal_text = ""
        my_formatos = ['standard', 'explorer', 'pioneer', 'modern', 'legacy', 'pauper', 'commander', 'oathbreaker', 'vintage', 'alchemy', 'historic', 'brawl', 'timeless']        
        for formato in my_formatos:
            cardLegality = card.legalities()[formato]
            if(cardLegality == "banned"):
                if(formato == "pauper" or formato == "vintage"):
                  legal_text += ':no_entry_sign: {}\n\n'.format(formato)      
                else:              
                    legal_text += ':no_entry_sign: {}\n'.format(formato)
            if(cardLegality == "not_legal"):
                if(formato == "pauper" or formato == "vintage"):
                  legal_text += ':radio_button: {}\n\n'.format(formato)      
                else:              
                    legal_text += ':radio_button: {}\n'.format(formato)                
            if(cardLegality == "legal"):
                if(formato == "pauper" or formato == "vintage"):
                    legal_text += ':white_check_mark: {}\n\n'.format(formato)      
                else:              
                    legal_text += ':white_check_mark: {}\n'.format(formato)                    
   
        # footer_list.append(InlineKeyboardButton("Legalities", callback_data=card.name()))
        footer_list.append(f'legalities: {legal_text}')
        # cacheable.CACHED_LEGALITIES.update({card.name(): legal_text})
        eur = '{}€'.format(card.prices(mode="eur")) if card.prices(mode="eur") is not None else "CardMarket"
        usd = '{}$'.format(card.prices(mode="usd")) if card.prices(mode="usd") is not None else "TCGPlayer"
        try:
            usd_link = card.purchase_uris().get("tcgplayer")
            eur_link = card.purchase_uris().get("cardmarket")
            # img_caption = emojize(":moneybag: [" + eur + "]" + "(" + eur_link + ")" + " | "
            #                       + "[" + usd + "]" + "(" + usd_link + ")" + "\n"
            #                       + legal_text, use_aliases=True)
        except KeyError:
            pass
            # img_caption = emojize(legal_text, use_aliases=True)

        try:
            card.card_faces()[0]['image_uris']
            is_flipcard = True
        except KeyError:
            is_flipcard = False
            pass

        if len(match) > 1 or is_flipcard:
            pass
            # if is_flipcard:
            #     photos.append(InputMediaPhoto(media=card.card_faces()[0]['image_uris']['normal'],
            #                                   caption=img_caption,
            #                                   parse_mode=telegram.ParseMode.MARKDOWN))
            #     photos.append(InputMediaPhoto(media=card.card_faces()[1]['image_uris']['normal'],
            #                                   caption=img_caption,
            #                                   parse_mode=telegram.ParseMode.MARKDOWN))
            # else:
            #     photos.append(InputMediaPhoto(media=card.image_uris(0, image_type="normal"),
            #                                   caption=img_caption,
            #                                   parse_mode=telegram.ParseMode.MARKDOWN))
            #     time.sleep(0.04)
            #     continue
        else:
            print(dir(card))
            print(card.image_uris())
            if card.related_uris().get("edhrec") is not None:
                # button_list.append(InlineKeyboardButton("Edhrec", url=card.related_uris().get("edhrec")))
                button_list.append(f'Edhred: {card.related_uris().get("edhrec")}')
            if card.related_uris().get("mtgtop8") is not None:
                # button_list.append(InlineKeyboardButton("Top8", url=card.related_uris().get("mtgtop8")))
                button_list.append(f'Top8: {card.related_uris().get("mtgtop8")}')
            # button_list.append(InlineKeyboardButton("Scryfall", url=card.scryfall_uri()))
            button_list.append(f'Scryfall: {card.scryfall_uri()}')
            if card.prices(mode="usd") is not None:
                # header_list.append(InlineKeyboardButton('{}$'.format(card.prices(mode="usd")),
                #                                         url=card.purchase_uris().get("tcgplayer")))
                header_list.append(f' {card.purchase_uris().get("tcgplayer")} ')
            else:
                # header_list.append(InlineKeyboardButton("TCGPlayer", url=usd_link))
                pass
            if card.prices(mode="eur") is not None:
                # header_list.append(InlineKeyboardButton('{}€'.format(card.prices(mode="eur")),
                #                                         url=card.purchase_uris().get("cardmarket")))
                header_list.append(f' {card.purchase_uris().get("cardmarket")} ')
            else:
                # header_list.append(InlineKeyboardButton("MKM", url=eur_link))
                pass
            # reply_markup = InlineKeyboardMarkup(util.build_menu(button_list,
            #                                                     header_buttons=header_list,
            #                                                     footer_buttons=footer_list,
            #                                                     n_cols=3))
            # context.bot.send_photo(chat_id=update.message.chat_id,
            #                        photo=card.image_uris(0, image_type="normal"),
            #                        parse_mode=telegram.ParseMode.MARKDOWN,
            #                        reply_markup=reply_markup,
            #                        reply_to_message_id=update.message.message_id)

            replymessage = '\n'.join(button_list).join(header_list).join(footer_list)
            print("DEBUG REPLY MESSAGE:")
            print(replymessage)
            return


if __name__ == '__main__':
    input = sys.argv[1]
    cards(input)