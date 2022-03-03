# def getEmbedsByLists(self, lists : list):
    def embeds_generator_by_lists(self, lists : list):
        embeds = []
        is_embed_instancing_now = True
        sum_size_of_embed = 0
        MAX_SIZE_OF_EMBED = 6000
        MAX_OF_ELEMENT = 10

        for i in range(0, len(lists), 1):
            sum_size_of_embed += len(lists[i][0]) + len(lists[i][1])
            print(str(sum_size_of_embed))
            # if len(embeds) >= max_of_element and sum_size_of_embed >= max_size_of_embed:
            #     print("上限超えちゃってるよ！")
            #     break
            if sum_size_of_embed >= MAX_SIZE_OF_EMBED:
                print("|||||||||||||||||||||||||||")
                embeds.append(copy.deepcopy(embed))
                if len(embeds) >= MAX_OF_ELEMENT:
                    print("上限超えちゃってるよ！")
#                     break
                    yield(embeds)
                embed = discord.Embed(title=lists[i][0], description=lists[i][1], color=0xff0000)
                sum_size_of_embed = 0
                # embed = ""
            if is_embed_instancing_now == True:
                embed = discord.Embed(title=lists[i][0], description=lists[i][1], color=0xff0000)
                is_embed_instancing_now = False
            else:
                embed.add_field(name=lists[i][0], value=lists[i][1], inline=False)
            print(i)
            if i == len(lists) - 1:
                embeds.append(copy.deepcopy(embed))

        yield(embeds)
