  let myChart = echarts.init(document.querySelector(".daily-count-chart"))
      let option = {
          xAxis: {
            type: 'category',
            data: []
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              data: [],
              type: 'line',
              smooth: true,
                color:'#2C82E5',
                markPoint: {
                data: [
                  { type: 'max', name: 'Max' },
                  { type: 'min', name: 'Min' }
                ]
              },
            }
          ]
        };
        window.addEventListener("resize", function() {
            myChart.resize();
          });

     $('.nav-item').on('click',function() {
         $(this).siblings().find("a").removeClass("active");
              // 为当前 <li> 元素的子 <a> 标签添加 active 类
              $(this).find("a").addClass("active");

              // 输出点击的 <li> 元素的 id
              var clickedItemId = $(this).find('a').attr("id");
              $("#" + clickedItemId + "_").show().siblings().hide();
     })

      $.get('/api/dailycount').then(function(res) {
          console.log(res)
          option.xAxis.data=res[0]
          option.series[0].data=res[1]
          myChart.setOption(option);

      })

    $.get('/api/pagecount').then(function(res) {
        $('#pagecount').text(res)
    })
      $.get('/api/linkcount').then(function(res) {
        $('#linkcount').text(res)
    })
        $.get('/api/scuessfail').then(function(res) {
            var successCount = res[200];
            var totalCount = res[200]+res[404];
            var successRate = (successCount / totalCount) * 100;
            successRate = successRate.toFixed(2);
            $('#scuessrate').text(successRate + "%")
    })