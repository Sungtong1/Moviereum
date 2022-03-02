<template>
  <div>
    <now-playings></now-playings>
    <popular-movie-list></popular-movie-list>
    <action-sf></action-sf>
    <romance-drama></romance-drama>
    <comedy-family></comedy-family>
    <criminal-thriller></criminal-thriller>
    <history-war></history-war>
    <horror-mystery></horror-mystery>
    <ani></ani>
  </div>
</template>

<script>
import NowPlayings from '@/components/NowPlayings'
import PopularMovieList from '@/components/PopularMovieList'
import ActionSf from '@/components/ActionSf'
import RomanceDrama from '@/components/RomanceDrama'
import ComedyFamily from '@/components/ComedyFamily'
import CriminalThriller from '@/components/CriminalThriller'
import HistoryWar from '@/components/HistoryWar'
import HorrorMystery from '@/components/HorrorMystery'
import Ani from '@/components/Ani'


export default {
  name: 'Home',
  components: {
    NowPlayings,
    PopularMovieList,
    ActionSf,
    RomanceDrama,
    ComedyFamily,
    CriminalThriller,
    HistoryWar,
    HorrorMystery,
    Ani,
  }
}
</script>

<style>
</style>